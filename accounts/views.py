from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DeleteView
from . import forms
from .models import User, Address
from .utils import RedirectAuthenticatedUserMixin


class UserSignUp(RedirectAuthenticatedUserMixin, CreateView):
    extra_context = {'title': 'Реєстрація'}
    template_name = 'accounts/signup.html'
    form_class = forms.UserRegisterForm
    redirect_authenticated_user_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return redirect('home')


class UserAuthentication(LoginView):
    extra_context = {'title': 'Вхід'}
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')


class PersonalCabinet(LoginRequiredMixin, TemplateView):
    extra_context = {'title': 'Особистий кабінет',
                     'subtitle': 'Керуйте своїми замовленнями та особистими даними'}
    template_name = 'accounts/personal_cabinet/personal_cabinet.html'


class PersonalInfoUpdateView(LoginRequiredMixin, UpdateView):
    extra_context = {'title': 'Особисті дані',
                     'subtitle': 'Керуйте своїми особистими та контактними даними'}
    template_name = 'accounts/personal_cabinet/personal_info.html'
    form_class = forms.UserForm
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class PersonalSafetyView(LoginRequiredMixin, TemplateView):
    extra_context = {'title': 'Безпека облікового запису',
                     'subtitle': 'Змінити пароль або видалити обліковий запис'}
    template_name = 'accounts/personal_cabinet/personal_safety.html'


class DeleteAccount(LoginRequiredMixin, DeleteView):
    extra_context = {'title': 'Видалення облікового запису'}
    success_url = reverse_lazy('login')

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class AddressesList(LoginRequiredMixin, ListView):
    extra_context = {'title': 'Мої адреси',
                     'subtitle': 'Керуйте своїми адресами та налаштуваннями доставки'}
    template_name = 'accounts/personal_cabinet/addresses_list.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddAddress(LoginRequiredMixin, CreateView):
    extra_context = {'title': 'Додавання адреси',
                     'subtitle': 'Додайте нову адресу та параметри доставки'}
    template_name = 'accounts/personal_cabinet/edit_addresses.html'
    form_class = forms.AddressForm
    success_url = reverse_lazy('addresses_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not Address.objects.filter(user=self.request.user, default_address=True):
            form.instance.default_address = True
        return super(AddAddress, self).form_valid(form)


class EditAddress(LoginRequiredMixin, UpdateView):
    extra_context = {'title': 'Редагування адреси',
                     'subtitle': 'Змініть адресу та параметри доставки'}
    template_name = 'accounts/personal_cabinet/edit_addresses.html'
    form_class = forms.AddressForm
    success_url = reverse_lazy('addresses_list')

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user, pk=self.kwargs['pk'])


@login_required
def set_default_address(request, pk):
    Address.objects.filter(user=request.user, default_address=True).update(default_address=False)
    Address.objects.filter(user=request.user, pk=pk).update(default_address=True)
    # previous_url = request.META.get("HTTP_REFERER")
    # if 'delivery_address' in previous_url:
    #     return redirect("checkout:delivery_address")
    return redirect('addresses_list')


@login_required
def delete_address(request, pk):
    Address.objects.get(user=request.user, pk=pk).delete()
    return redirect('addresses_list')
