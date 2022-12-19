from django.contrib import admin
from forum.models import Post, Topic, CategoryDetail, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(CategoryDetail)
class CategoryDetailAdmin(admin.ModelAdmin):
    list_display = ['detail_title', 'category', 'description']
    list_filter = ['category']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_detail']
    list_filter = ['category_detail']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['topic', 'created', 'published', 'author']
    list_filter = ['created', 'topic']

