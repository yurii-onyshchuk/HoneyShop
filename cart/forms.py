from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.HiddenInput, initial=1)


class CartAddSeveralProductForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), min_value=1, max_value=20,
                                  initial=1, label='')
