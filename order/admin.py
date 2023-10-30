from django.contrib import admin

from order.models import Order, OrderItem


class OrderItemAdmin(admin.ModelAdmin):
    """Admin configuration for managing individual order items."""

    pass


class OrderItemInline(admin.TabularInline):
    """Inline representation of order items within the order administration."""

    model = OrderItem
    extra = 0
    readonly_fields = ['price']


class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for managing orders."""

    readonly_fields = ['total_price']
    inlines = [OrderItemInline, ]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
