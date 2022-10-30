from django.contrib import admin
from .models import User, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'slug']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass