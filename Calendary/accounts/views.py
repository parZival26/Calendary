from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from .forms import UserCreationForm


class Login(LoginView):
    redirect_authenticated_user = True
    template_name = "accounts/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'login'
        return context
    
class Register(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/form.html"
    success_url = reverse_lazy('list tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

@login_required
def log_out(request):
    logout(request)
    return redirect('login')
