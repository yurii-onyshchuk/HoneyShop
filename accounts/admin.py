from django.contrib import admin

from .models import User, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for the User model.

    Defines the display fields and links for the User model in the admin panel.
    """

    list_display = ['email', 'first_name', 'last_name', 'phone_number', 'slug', ]
    list_display_links = ['email', ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin configuration for the Address model."""

    pass
