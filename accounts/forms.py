import re

from allauth.socialaccount.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm

from phonenumber_field.formfields import PhoneNumberField

from .models import User, Address


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': False})
        self.fields['email'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def save(self, commit=True):
        data = self.cleaned_data.copy()
        email = data.pop('email')
        phone_number = data.pop('phone_number')
        password = data.pop('password1')
        data.pop('password2')
        user = get_user_model().objects.create_user(email, phone_number, password, **data)
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')


class SocialSignUpForm(SignupForm, forms.ModelForm):
    email = forms.EmailField(widget=forms.HiddenInput)
    phone_number = forms.CharField(label='Номер телефону')

    def save(self, request):
        user = super().save(request)
        user.phone_number = self.cleaned_data['phone_number']
        user.set_unusable_password()
        user.save()
        return user

    class Meta:
        model = User
        fields = ('phone_number',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email або номер телефону')

    def clean_username(self):
        username = self.cleaned_data['username']
        if re.match(r'^[\d\+\-\(\) ]+$', username):
            phone_number = PhoneNumberField().clean(username)
            return str(phone_number)
        else:
            return username


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_of_birth', 'email', 'phone_number',)
        widgets = {'date_of_birth': forms.DateInput()}


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'default_address']
