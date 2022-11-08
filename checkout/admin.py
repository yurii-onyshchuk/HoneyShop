from django.contrib import admin

from checkout.models import DeliveryOptions, PaymentOptions

admin.site.register(DeliveryOptions)
admin.site.register(PaymentOptions)
