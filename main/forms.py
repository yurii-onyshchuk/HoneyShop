from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(), label="Ваше ім'я")
    email = forms.EmailField(widget=forms.EmailInput(), label="E-mail")
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}), label="Повідомлення")
