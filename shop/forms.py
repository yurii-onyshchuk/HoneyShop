from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': '10'}), label='', min_length=5, max_length=500)

    class Meta:
        model = Review
        fields = ('body',)
