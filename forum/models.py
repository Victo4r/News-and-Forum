from django.utils import timezone

from django.db import models
from users.models import User


class Category(models.Model):
    title = models.CharField(
        max_length=48, blank=True, null=True
    )

    def __str__(self):
        return f'{self.title}'


class CategoryDetail(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True
                                 , related_name='children'
                                 )
    detail_title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.detail_title}'


class Topic(models.Model):
    category_detail = models.ForeignKey(
        CategoryDetail, on_delete=models.CASCADE, blank=True, null=True, related_name='topics'
    )
    title = models.CharField(
        max_length=100, verbose_name='Заголовок', blank=True, null=True
    )
    additional_info = models.TextField(blank=True, null=True
                                       )


    def __str__(self):
        return f'{self.title}'


class Post(models.Model):
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, verbose_name='Тема', related_name='posts'
    )
    text = models.TextField(
        verbose_name='текст'
    )
    created = models.DateTimeField(
        verbose_name='дата создания',
        default=timezone.now()
    )
    published = models.DateTimeField(
        verbose_name='дата публикации',
        default=timezone.now()
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        blank=True, null=True
    )

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return f'{self.text}'