from datetime import datetime
from datetime import timedelta

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib import messages

from forum.models import Category, CategoryDetail, Topic, Post
from forum.forms import PostForm, TopicForm, EmailPostForm


def category_list(request):
    categories = Category.objects.all()
    main_topics = Topic.objects.annotate(num_posts=Count('posts')).filter(num_posts__gte=1).order_by('-num_posts')[:6]
    return render(request, 'forum/category_list.html',
                  {
                      'categories': categories,
                      'main_topics': main_topics
                  })


def topic_list(request, detail_pk):
    parent_topic = CategoryDetail.objects.get(pk=detail_pk)
    topics = Topic.objects.filter(category_detail=detail_pk)
    counter_topics = topics.count()
    paginator = Paginator(topics, 10)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    if request.method == 'POST':
        topic_form = TopicForm(request.POST)
        if topic_form.is_valid():
            topic = topic_form.save(commit=False)
            topic.author = request.user
            topic.category_detail = CategoryDetail.objects.filter(pk=detail_pk).first()
            topic.save()
            return redirect('forum:topic_list', detail_pk=parent_topic.pk)
    else:
        topic_form = TopicForm()
    return render(request, 'forum/topic_list.html', {'parent_topic': parent_topic,
                                                     'topics': topics,
                                                     'topic_form': topic_form,
                                                     'counter_topics': counter_topics,
                                                     'page': page
                                                     })


def topic_detail(request, topic_pk):
    topic = Topic.objects.get(pk=topic_pk)
    posts = Post.objects.filter(topic=topic_pk)
    counter = posts.count()
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)
    is_paginated = page.has_other_pages()
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.published = datetime.now()
            post.topic = Topic.objects.filter(pk=topic_pk).first()
            post.save()
            return redirect('forum:topic_detail', topic_pk=topic.pk)
    else:
        post_form = PostForm()
    context = {
                   'topic': topic,
                   'posts': posts,
                   'counter': counter,
                   'post_form': post_form,
                   'page': page,
                   'is_paginated': is_paginated,
                   }
    return render(request, 'forum/topic_detail.html', context)


def topic_filter_new(request):
    now = datetime.now()
    day_ago = now - timedelta(days=1)
    new_topics = Topic.objects.filter(posts__created__gte=day_ago)
    context = {
        'new_topics': new_topics
    }
    return render(request, 'forum/topic_filter_new.html', context)



def topic_filter_takepart(request):
    take_part_topics = Topic.objects.filter(posts__author=request.user)
    context = {
        'take_part_topics': take_part_topics
    }
    return render(request, 'forum/topic_filter_takepart.html', context)


def complain(request, post_pk):
    post = Post.objects.filter(pk=post_pk).first()
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            subject = (form.cleaned_data['name'], form.cleaned_data['email'])
            post_text = post.text
            complain_text = (form.cleaned_data['comments'])
            massage = "Сообщение форума {} вызвало жалобу {}".format(post_text, complain_text)
            mail = send_mail(subject, massage, 'usermail.2022@ukr.net', ['info@ukr.net'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('forum:complain', post_pk=post.pk)
            else:
                messages.error(request, 'Ошибка отправки')
    else:
        form = EmailPostForm()
    context = {
        'post': post,
        'form': form
               }
    return render(request, 'forum/complain.html', context)
