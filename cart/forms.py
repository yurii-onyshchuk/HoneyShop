from django import forms
from django.core.exceptions import ValidationError

from shop.models import Product
from .widgets import CartProductNumberInput


class CartUpdateProductForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    quantity = forms.IntegerField(widget=CartProductNumberInput(), label='', initial=1, min_value=1, max_value=20, )

    def clean_quantity(self):
        product_id = self.fields['product_id'].value
        quantity = self.cleaned_data['quantity']
        product = Product.objects.get(id=product_id)
        available_quantity = product.quantity
        if quantity > available_quantity:
            raise ValidationError(f'На даний момент доступно тільки {int(product.quantity)} шт. товару "{product}"')
        else:
            return quantity
