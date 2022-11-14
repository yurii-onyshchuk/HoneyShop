from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Ваше ім'я")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label="E-mail")
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
                              label="Повідомлення")
