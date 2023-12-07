from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied
from .models import Task
from .forms import TaskForm

class ListTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "eventhub/list.html"

    def get_queryset(self):
        return Task.objects.filter(users=self.request.user).order_by('-due_date')


class CreateTasksView(LoginRequiredMixin, CreateView):
    template_name = "eventhub/form.html"
    form_class = TaskForm
    model = Task
    
    def get_success_url(self):
        return reverse_lazy("list tasks")
    
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

    def get_success_url(self):
        return reverse_lazy("list tasks")
    
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

    def get_success_url(self):
        return reverse_lazy("list tasks")