from django import forms
from forum.models import Topic, Post
from django.forms import ModelForm, Textarea


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = (
            'text',
        )
        widgets = {
            'text': Textarea(attrs={'rows': 4, 'cols': 60}),
        }


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = (
            'title',
        )
        widgets = {
            'title': Textarea(attrs={'rows': 1})
        }


class EmailPostForm (forms.Form):
    name = forms.CharField(max_length=48)
    email = forms.EmailField()
    comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 5}))
