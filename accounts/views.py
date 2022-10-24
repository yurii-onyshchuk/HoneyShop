from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from . import forms
from .models import User


class UserRegister(CreateView):
    extra_context = {'title': 'Реєстрація'}
    template_name = 'accounts/register.html'
    form_class = forms.UserRegisterForm
    success_url = reverse_lazy('index')


class UserAuthentication(LoginView):
    extra_context = {'title': 'Вхід'}
    template_name = 'accounts/login.html'
    form_class = forms.UserAuthenticationForm
    success_url = reverse_lazy('index')


class UserSettingsView(LoginRequiredMixin, UpdateView):
    extra_context = {'title': 'Особиста інформація'}
    template_name = 'accounts/settings.html'
    form_class = forms.UserSettingForm
    success_url = reverse_lazy('home')
    model = User

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)
