from django.contrib import admin

from order.models import Order, OrderItem


class OrderItemAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price']


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['total_price']
    inlines = [OrderItemInline, ]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
