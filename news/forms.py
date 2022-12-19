from django import forms

from news.models import Comments


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = (
            'text',
        )
        widgets = {
            'text': forms.Textarea(attrs={'cols': 75, 'rows': 1})
        }
