from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DeleteView

from . import forms
from .models import User, Address
from .mixins import RedirectAuthenticatedUserMixin


class SignUpView(RedirectAuthenticatedUserMixin, CreateView):
    """View for handling the user registration."""

    extra_context = {'title': 'Реєстрація'}
    template_name = 'accounts/signup.html'
    form_class = forms.SignUpForm
    redirect_authenticated_user_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user, backend='accounts.backends.EmailPhoneNumberBackend')
            messages.success(self.request, 'Успішна реєстрація!')
        return redirect('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Помилка реєстрації!')
        return super(SignUpView, self).form_invalid(form)


class CustomLoginView(LoginView):
    """View for handling the user login process."""

    extra_context = {'title': 'Вхід'}
    template_name = 'accounts/login.html'
    form_class = forms.LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')


class PersonalCabinetView(LoginRequiredMixin, TemplateView):
    """View for the user's personal cabinet.

    This view displays the user's personal cabinet with information
    about orders and personal data.
    """

    extra_context = {'title': 'Особистий кабінет',
                     'subtitle': 'Керуйте своїми замовленнями та особистими даними'}
    template_name = 'accounts/personal_cabinet/personal_cabinet.html'


class PersonalInfoUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating the user's personal information."""

    extra_context = {'title': 'Особисті дані',
                     'subtitle': 'Керуйте своїми особистими та контактними даними'}
    template_name = 'accounts/personal_cabinet/personal_info.html'
    form_class = forms.UserForm

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_success_url(self):
        messages.success(self.request, 'Особисті дані успішно змінено!')
        return reverse_lazy('personal_cabinet')


@login_required
def user_avatar_change(request):
    """View for changing the user's avatar photo."""
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        user.photo = request.FILES['user_photo']
        user.save_thumbnail()
    return redirect('personal_info', slug=request.user.slug)


@login_required
def user_avatar_delete(request):
    """ View for deleting the user's avatar photo."""
    if request.method == 'POST':
        User.objects.get(pk=request.user.pk).photo.delete(save=True)
    return redirect('personal_info', slug=request.user.slug)


class PersonalSafetyView(LoginRequiredMixin, TemplateView):
    """View for account safety settings."""

    extra_context = {'title': 'Безпека облікового запису',
                     'subtitle': 'Змінити пароль або видалити обліковий запис'}
    template_name = 'accounts/personal_cabinet/personal_safety.html'


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting a user's account."""

    extra_context = {'title': 'Видалення облікового запису'}

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_success_url(self):
        messages.success(self.request, 'Акаунт успішно видалено!')
        return reverse_lazy('login')


class AddressesListView(LoginRequiredMixin, ListView):
    """View for displaying a user's address list."""

    extra_context = {'title': 'Мої адреси',
                     'subtitle': 'Керуйте своїми адресами та налаштуваннями доставки'}
    template_name = 'accounts/personal_cabinet/addresses_list.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddAddressView(LoginRequiredMixin, CreateView):
    """View for adding a new address for the user."""

    extra_context = {'title': 'Додавання адреси',
                     'subtitle': 'Додайте нову адресу та параметри доставки'}
    template_name = 'accounts/personal_cabinet/edit_addresses.html'
    form_class = forms.AddressForm
    success_url = reverse_lazy('addresses_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not Address.objects.filter(user=self.request.user, default_address=True):
            form.instance.default_address = True
        return super(AddAddressView, self).form_valid(form)


class EditAddressView(LoginRequiredMixin, UpdateView):
    """View for editing an existing address for the user."""

    extra_context = {'title': 'Редагування адреси',
                     'subtitle': 'Змініть адресу та параметри доставки'}
    template_name = 'accounts/personal_cabinet/edit_addresses.html'
    form_class = forms.AddressForm
    success_url = reverse_lazy('addresses_list')

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user, pk=self.kwargs['pk'])


@login_required
def set_default_address(request, pk):
    """View for setting an address as the default address."""
    Address.objects.filter(user=request.user, default_address=True).update(default_address=False)
    Address.objects.filter(user=request.user, pk=pk).update(default_address=True)
    return redirect('addresses_list')


@login_required
def delete_address(request, pk):
    """View for deleting an address."""
    Address.objects.get(user=request.user, pk=pk).delete()
    return redirect('addresses_list')
