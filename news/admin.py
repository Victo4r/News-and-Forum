from django.contrib import admin
from django import forms
from news.models import Category, News, Comments, Like
from ckeditor_uploader.widgets import CKEditorUploadingWidget

admin.site.register(Category)
admin.site.register(Like)


class NewsAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = [
        'title',
        'category',
        'published_date',
    ]
    list_filter = [
        'published_date',
        'category',
    ]
    search_fields = [
        'published_date',
        'title',
        'category__title'
    ]


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'text',
        'author',
        'article',
        'created_date'
    ]
    search_fields = [
        'author__username',
        'created_date',
        'article__title'
    ]
    list_filter = [
        'author__username',
        'created_date',
        'article'
    ]
