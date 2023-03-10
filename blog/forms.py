from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=500, widget=forms.Textarea(
        attrs={'id': 'contactcomment', 'rows': '3', 'placeholder': 'Ваш коментар...'}), )

    class Meta:
        model = Comment
        fields = ('body',)
