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

    def clean_city(self):
        cleaned_data = super().clean()
        if cleaned_data['delivery_option'].method == 'DELIVERY_SERVICE' or 'HOME_DELIVERY':
            if not cleaned_data['city']:
                raise forms.ValidationError('Вкажіть місто доставки')

    def clean_street(self):
        cleaned_data = super().clean()
        if cleaned_data['delivery_option'].method == 'HOME_DELIVERY':
            if not cleaned_data['street']:
                raise forms.ValidationError('Вкажіть вулицю доставки')

    def clean_house(self):
        cleaned_data = super().clean()
        if cleaned_data['delivery_option'].method == 'HOME_DELIVERY':
            if not cleaned_data['house']:
                raise forms.ValidationError('Вкажіть будинок доставки')

    def clean_delivery_service_department(self):
        cleaned_data = super().clean()
        if cleaned_data['delivery_option'].method == 'DELIVERY_SERVICE':
            if not cleaned_data['delivery_service_department']:
                raise forms.ValidationError('Вкажіть відділення служби доставки')

    class Meta:
        model = Order
        exclude = ['user', 'total_price', 'billing_status']
