from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.HiddenInput, initial=1)
