from django import forms

from checkout.models import PaymentOptions, DeliveryOptions
from external_api_services.widgets import CityAutocompleteWidget, DepartmentAutocompleteWidget, StreetAutocompleteWidget
from order.models import Order


class CheckoutForm(forms.ModelForm):
    """Form for processing order checkout information.

    This form is used to collect and validate user input
    for processing an order checkout.
    """

    def __init__(self, *args, **kwargs):
        """Сustomization of the CheckoutForm by setting specific field options and querysets
        for the "delivery_option" and "payment_option" fields.
        It also sets the "empty_label" for these fields to not displayed with an empty choice.
        """
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['delivery_option'].empty_label = None
        self.fields['payment_option'].empty_label = None
        self.fields['payment_option'].queryset = PaymentOptions.objects.filter(is_active=True)
        self.fields['delivery_option'].queryset = DeliveryOptions.objects.filter(is_active=True)

    def clean_city(self):
        """Validate the city field based on the selected delivery option.

        This method checks the city field for required input based on the
        chosen delivery option.
        """
        cleaned_data = super().clean()
        if cleaned_data['delivery_option'].method != 'IN_STORE':
            if not cleaned_data['city']:
                raise forms.ValidationError('Вкажіть місто доставки')
            return cleaned_data['city']

    def clean_street(self):
        """Validate the street field for home delivery.

        This method checks the street field for required input
        when the "HOME_DELIVERY" method is chosen.
        """
        cleaned_data = super().clean()
        if cleaned_data['delivery_option'].method == 'HOME_DELIVERY':
            if not cleaned_data['street']:
                raise forms.ValidationError('Вкажіть вулицю доставки')
            return cleaned_data['street']

    def clean_house(self):
        """Validate the house field for home delivery.

        This method checks the house field for required input
        when the "HOME_DELIVERY" method is chosen.
        """
        cleaned_data = super().clean()
        if cleaned_data['delivery_option'].method == 'HOME_DELIVERY':
            if not cleaned_data['house']:
                raise forms.ValidationError('Вкажіть будинок доставки')
            return cleaned_data['house']

    def clean_flat(self):
        """Validate the flat field for home delivery."""

        cleaned_data = super().clean()
        if cleaned_data['delivery_option'].method == 'HOME_DELIVERY':
            return cleaned_data['flat']

    def clean_delivery_service_department(self):
        """Validate the delivery service department field for delivery service method.

        This method checks the delivery service department field for required input
        when the "DELIVERY_SERVICE" method is chosen.
        """
        cleaned_data = super().clean()
        if cleaned_data['delivery_option'].method == 'DELIVERY_SERVICE':
            if not cleaned_data['delivery_service_department']:
                raise forms.ValidationError('Вкажіть відділення служби доставки')
            return cleaned_data['delivery_service_department']

    class Meta:
        model = Order
        exclude = ['user', 'total_price', 'billing_status']
        widgets = {'city': CityAutocompleteWidget(attrs={'autocomplete': 'off', }),
                   'street': StreetAutocompleteWidget(attrs={'autocomplete': 'off', }),
                   'delivery_service_department': DepartmentAutocompleteWidget(attrs={'autocomplete': 'off', })}
