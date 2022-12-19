from django.db import models
from users.models import User


class Category(models.Model):
    title = models.CharField(
        max_length=64,
        verbose_name='Title',
    )
    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return f'{self.title}'


class News(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Category',
    )
    title = models.CharField(
        max_length=88,
        verbose_name='Title',
    )
    text = models.TextField(
        verbose_name='Text'
    )
    published_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Published date'
    )
    main_image = models.ImageField(
        upload_to='news',
        verbose_name='Main image'
    )

    def __str__(self):
        return f'{self.title}'


class Comments(models.Model):
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='Replies',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='Comments'
    )
    article = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='Comments',
        verbose_name='Article'
    )
    text = models.TextField(
        verbose_name='Text',
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created date',
    )
    comment_like = models.IntegerField(
        verbose_name='Like',
        default=0,
    )
    comment_dislike = models.IntegerField(
        verbose_name='Dislike',
        default=0,
    )

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f'{self.author}, {self.text}'


class Like(models.Model):
    VOTES = (
       ('LIKE', 'like'),
       ('DISLIKE', 'dislike'),
       (None, 'None'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name='Like',
    )
    comment = models.ForeignKey(
        Comments,
        on_delete=models.CASCADE,
        verbose_name='Comment',
        related_name='Like',
    )
    like_or_dislike = models.CharField(
        max_length=7,
        choices=VOTES,
        default=None
    )

    def __str__(self):
        return f'{self.like_or_dislike}'
