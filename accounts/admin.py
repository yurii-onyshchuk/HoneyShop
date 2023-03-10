from django.contrib import admin
from .models import User, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone_number', 'slug', ]
    list_display_links = ['email', ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
