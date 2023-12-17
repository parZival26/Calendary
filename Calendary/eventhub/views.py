from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.http import Http404, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, TemplateView, DetailView
from django.core.exceptions import PermissionDenied
from .models import Tag, Task
from django.contrib.sites.shortcuts import get_current_site
from .forms import TagForm, TaskForm
from calendar import SUNDAY, month, monthcalendar, setfirstweekday
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.contrib import messages
from .utils import send_email
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'eventhub/calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = int(self.kwargs.get('year', datetime.now().year))
        month = int(self.kwargs.get('month', datetime.now().month))

        setfirstweekday(SUNDAY)
        cal = monthcalendar(year, month)

        for week in cal:
            for i, day in enumerate(week):
                if day != 0:
                    week[i] = datetime(year, month, day)

        month_name = datetime(year, month, 1).strftime('%B')

        context['calendar'] = cal
        context['month_name'] = month_name
        context['year'] = year

        return context

class ListTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "eventhub/list.html"

    def get_queryset(self):

        # Validar que se proporcionó el parámetro day en la URL
        year = int(self.kwargs.get('year', datetime.now().year))
        month = int(self.kwargs.get('month', datetime.now().month))
        day = int(self.kwargs.get('day', datetime.now().day))

        # Validar que se proporcionó el parámetro day en la URL
        if not (day and month and year):
            raise Http404("Los parámetros 'day', 'month' y 'year' son obligatorios en la URL.")

        # Convertir los valores de year, month y day a un objeto datetime
        start_date = timezone.make_aware(timezone.datetime(year, month, day))
        end_date = start_date + timezone.timedelta(days=1)

        # Filtrar las tareas por usuario, año, mes y día
        return Task.objects.filter(users=self.request.user, due_date__range=(start_date, end_date))    

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset().filter(users=self.request.user)
        state = self.request.GET.getlist('state')
        tags = self.request.GET.getlist('tags')
        date_range = self.request.GET.get('date_range')
        date_interval = self.request.GET.get('date_interval')
        if state:
            queryset = queryset.filter(state__in = state)
        if tags:
            queryset = queryset.filter(tags__name__in=tags)
        if date_range:
            today = timezone.now().date()

            if date_range == 'today':
                end_date = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time())) + timezone.timedelta(days=1)
                queryset = queryset.filter(due_date__range=[today, end_date])
            elif date_range == 'this_week':
                start_week = timezone.make_aware(timezone.datetime.combine(today - timedelta(days=today.weekday()), timezone.datetime.min.time()))
                end_week = start_week + timedelta(days=6)
                queryset = queryset.filter(due_date__range=[start_week, end_week])
            elif date_range == 'this_month':
                first_day_of_month = timezone.make_aware(timezone.datetime.combine(today.replace(day=1), timezone.datetime.min.time()))
                # Obtener el último día del mes actual
                last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                
                queryset = queryset.filter(due_date__range=[first_day_of_month, last_day_of_month])

        if date_interval:
            today = timezone.now().date()
            end_date = (timezone.make_aware(datetime.strptime(date_interval, '%Y-%m-%d')) + timedelta(days=1)).date()
            if end_date < today:
                print("La fecha final es anterior a la fecha actual. No se puede filtrar en el pasado.")
            else:
                print(f"today: {today}, end_date: {end_date}")
                queryset = queryset.filter(due_date__range=[today, end_date])

        return queryset.order_by('due_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['states'] = Task.STATE_CHOICES
        context['tags'] = Tag.objects.filter(users=self.request.user)
        return context
        
class CreateTasksView(LoginRequiredMixin, CreateView):
    template_name = "eventhub/form.html"
    form_class = TaskForm
    model = Task
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Tarea"
        context['form_action'] = reverse('create task')
        context['id'] = "createTaskForm"
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        send_email(self.object, self.request.user)
        response_data = {'message': 'Tarea creada exitosamente'}
        return JsonResponse(response_data)


    def form_invalid(self, form):
        response_data = {'message': 'Hubo un error al crear la tarea'}
        return JsonResponse(response_data, status=400)
    
    def get_success_url(self):
        messages.success(self.request, 'Tarea creada exitosamente')
        return reverse_lazy('list tasks', kwargs={'year': self.object.due_date.year, 'month': self.object.due_date.month, 'day': self.object.due_date.day})

class UpdateTasksView(LoginRequiredMixin, UpdateView):
    template_name =  "eventhub/form.html"
    form_class = TaskForm
    model = Task
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Verificar si el usuario tiene acceso al objeto
        if obj.users.filter(pk=self.request.user.pk).exists():
            return obj
        else:
            raise PermissionDenied("No tienes permisos para acceder a esta tarea.")

    def form_valid(self, form):
        self.object = form.save()
        response_data = {'message': 'Tarea Actualizada exitosamente'}
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = {'message': 'Hubo un error al actualizar la tarea'}
        return JsonResponse(response_data, status=400)
    
    def get_success_url(self):
        messages.success(self.request, 'Tarea actualizada exitosamente')
        return reverse_lazy('list tasks', kwargs={'year': self.object.due_date.year, 'month': self.object.due_date.month, 'day': self.object.due_date.day})
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs.get('pk')
        context['title'] = "Actualizar Tarea"
        context['form_action'] = reverse('update task', kwargs={'pk': task_id})
        context['id'] = 'updateTaskForm'
        return context
    
class DeleteTasksView(LoginRequiredMixin, DeleteView):
    template_name = "eventhub/form.html"
    model = Task

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Verificar si el usuario tiene acceso al objeto
        if obj.users.filter(pk=self.request.user.pk).exists():
            return obj
        else:
            raise PermissionDenied("No tienes permisos para acceder a esta tarea.")
        
    def form_valid(self, form):
        self.get_object().delete()
        response_data = {'message': 'Tarea eliminada exitosamente'}
        return JsonResponse(response_data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs.get('pk')
        context['title'] = "Eliminar Tarea"
        context['form_action'] = reverse('delete task', kwargs={'pk': task_id})
        context['id'] = 'deleteTaskForm'
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Tarea eliminada exitosamente')
        return reverse_lazy('list tasks', kwargs={'year': self.object.due_date.year, 'month': self.object.due_date.month, 'day': self.object.due_date.day})

class ListTagsView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "eventhub/tags.html"

    def get_queryset(self):
        return Tag.objects.filter(users=self.request.user)
        
class CreateTagView(LoginRequiredMixin, CreateView):
    template_name = "eventhub/form.html"
    form_class = TagForm
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Etiqueta"
        context['form_action'] = reverse('create tag')
        context['id'] = 'createTagForm'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        response_data = {'message': 'Etiqueta creada exitosamente'}
        return JsonResponse(response_data)
    
    def form_invalid(self, form):
        response_data = {'message': 'Hubo un error al crear la tarea'}
        return JsonResponse(response_data, status=400)
    
    def get_success_url(self):
        messages.success(self.request, 'Etiqueta creada exitosamente')
        return reverse_lazy('list tags')
    
class UpdateTagView(LoginRequiredMixin, UpdateView):
    template_name = "eventhub/form.html"
    form_class = TagForm
    model = Tag
    success_url = 'list tags'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Verificar si el usuario tiene acceso al objeto
        if obj.users.filter(pk=self.request.user.pk).exists():
            return obj
        else:
            raise PermissionDenied("No tienes permisos para acceder a esta Etiqueta.")

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('pk')
        context['title'] = "Actualizar Etiqueta"
        context['form_action'] = reverse('update tag', kwargs={'pk': tag_id })
        context['id'] = 'updateTagForm'
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        response_data = {'message': 'Etiqueta Actualizada exitosamente'}
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = {'message': 'Hubo un error al actualizar la Etiqueta'}
        return JsonResponse(response_data, status=400)
    
class DeleteTagView(LoginRequiredMixin, DeleteView):
    template_name = "eventhub/form.html"
    model = Tag
    success_url = 'list tags'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.users.filter(pk=self.request.user.pk).exists():
            return obj 
        else:
            raise PermissionDenied("No tienes permisos para acceder a esta Etiqueta.")
        
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('pk')
        context['title'] = "Eliminar Etiqueta"
        context['form_action'] = reverse('delete tag', kwargs={'pk': tag_id})
        context['id'] = 'deleteTagForm'
        return context
    
    def form_valid(self, form):
        self.get_object().delete()
        response_data = {'message': 'Etiqueta eliminada exitosamente'}
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = {'message': 'Hubo un error al eliminada la Etiqueta'}
        return JsonResponse(response_data, status=400)
        

class ShareTaskView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'eventhub/share_task.html'

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        current_site = get_current_site(request)
        domain = current_site.domain
        shared_link = request.build_absolute_uri(reverse('share_task_with_user', kwargs={'pk': task.pk}))

        return render(request, self.template_name, {'task': task, 'shared_link': shared_link, 'domain': domain})
    
@login_required
def share_task_with_user(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    # Agrega el usuario actual a la lista de usuarios compartidos
    task.users.add(request.user)
    
    # Redirige a la página de compartir tarea
    return redirect('share_task', pk=pk)