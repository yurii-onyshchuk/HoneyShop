import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from phonenumber_field.formfields import PhoneNumberField
from .models import User, Address


class UserSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
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


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email або номер телефону')

    def clean_username(self):
        username = self.cleaned_data['username']
        if re.match(r'^[\d\+\-\(\) ]+$', username):
            phone_number = PhoneNumberField().clean(username)
            return str(phone_number)
        else:
            return username


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''


class UserPasswordChangeForm(PasswordChangeForm):
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
