
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, TemplateView
from django.core.exceptions import PermissionDenied
from .models import Tag, Task
from .forms import TagForm, TaskForm
from calendar import SUNDAY, month, monthcalendar, setfirstweekday
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages
from .utils import send_email

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
        due_date = timezone.datetime(year, month, day)

        # Filtrar las tareas por usuario, año, mes y día
        return Task.objects.filter(users=self.request.user, due_date=due_date)
    
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset().filter(users=self.request.user)
        state = self.request.GET.getlist('state')
        tags = self.request.GET.getlist('tags')
        date_range = self.request.GET.get('date_range')
        if state:
            queryset = queryset.filter(state__in = state)
        if tags:
            queryset = queryset.filter(tags__name__in=tags)
        if date_range:
            today = timezone.now().date()

            if date_range == 'today':
                queryset = queryset.filter(due_date=today)
            elif date_range == 'this_week':
                start_week = today - timedelta(days=today.weekday())
                end_week = start_week + timedelta(days=6)
                queryset = queryset.filter(due_date__range=[start_week, end_week])
            elif date_range == 'this_month':
                first_day_of_month = today.replace(day=1)
                # Obtener el último día del mes actual
                last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                
                queryset = queryset.filter(due_date__range=[first_day_of_month, last_day_of_month])

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