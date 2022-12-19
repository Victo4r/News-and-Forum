# Generated by Django 4.1.3 on 2022-12-13 11:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=48, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_title', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='текст')),
                ('created', models.DateTimeField(default=datetime.datetime(2022, 12, 13, 11, 52, 30, 627214, tzinfo=datetime.timezone.utc), verbose_name='дата создания')),
                ('published', models.DateTimeField(default=datetime.datetime(2022, 12, 13, 11, 52, 30, 627214, tzinfo=datetime.timezone.utc), verbose_name='дата публикации')),
            ],
            options={
                'ordering': ['-published'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Заголовок')),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('category_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='forum.categorydetail')),
            ],
        ),
    ]
