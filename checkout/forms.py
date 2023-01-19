from django import forms

from order.models import Order
from checkout.models import PaymentOptions, DeliveryOptions


class CheckoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['delivery_option'].empty_label = None
        self.fields['payment_option'].empty_label = None
        self.fields['payment_option'].queryset = PaymentOptions.objects.filter(is_active=True)
        self.fields['delivery_option'].queryset = DeliveryOptions.objects.filter(is_active=True)

    class Meta:
        model = Order
        exclude = ['user', 'total_price', 'billing_status']
