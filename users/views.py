from django.contrib.auth.views import (LoginView, PasswordResetView,
                                       PasswordChangeView)
from django.urls import reverse_lazy
from django.views.generic import CreateView


from .forms import CreationForm


class Register(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/Registration.html'


class Login(LoginView):
    success_url = reverse_lazy('index')
    template_name = 'users/AuthForm.html'


class ChangePassword(PasswordChangeView):
    template_name = 'users/ChangePassword.html'


class ResetPassword(PasswordResetView):
    template_name = 'users/ResetPassword.html'
