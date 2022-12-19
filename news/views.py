from django.shortcuts import render, get_object_or_404, redirect

from news.models import Category, News, Comments, Like
from news.forms import CommentForm


def category():
    category = Category.objects.all()
    return category


def news_list(request):
    news = News.objects.all().order_by('-published_date')
    context = {
        'news': news,
        'categories': category(),
    }
    return render(request, 'news/news_list.html', context)


def news_in_category(request, slug):
    cat = Category.objects.get(slug=slug)
    news = News.objects.filter(category=cat).order_by('-published_date')
    context = {
        'news': news,
        'categories': category(),
    }
    return render(request, 'news/news_list.html', context)


def create_comment(request, item):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None
        if parent_id:
            parent_obj = Comments.objects.get(id=parent_id)
            if parent_obj:
                replay_comment = comment_form.save(commit=False)
                replay_comment.parent = parent_obj
        new_comment = comment_form.save(commit=False)
        new_comment.article = item
        new_comment.author = request.user
        new_comment.save()
        return new_comment


def like_or_dislike(request, news_pk, comment_pk, vote):
    items = get_object_or_404(News, pk=news_pk)
    comment = get_object_or_404(Comments, pk=comment_pk)
    old_like = Like.objects.filter(user=request.user, comment=comment_pk)
    if old_like:
        like = Like.objects.get(user=request.user, comment=comment_pk)
        if like.like_or_dislike == 'like' and vote == 'like':
            like.delete()
            comment.comment_like -= 1
            comment.save()
        elif like.like_or_dislike == 'dislike' and vote == 'dislike':
            like.delete()
            comment.comment_dislike -= 1
            comment.save()
        elif like.like_or_dislike == 'like' and vote == 'dislike':
            like.like_or_dislike = 'dislike'
            like.save()
            comment.comment_dislike += 1
            comment.comment_like -= 1
            comment.save()
        elif like.like_or_dislike == 'dislike' and vote == 'like':
            like.like_or_dislike = 'like'
            like.save()
            comment.comment_dislike -= 1
            comment.comment_like += 1
            comment.save()
    else:
        new_like = Like.objects.create(
            user=request.user,
            comment=comment,
            like_or_dislike=vote,
        )
        new_like.save()
        if vote == 'like':
            comment.comment_like += 1
            comment.save()
        elif vote == 'dislike':
            comment.comment_dislike += 1
            comment. save()
    return redirect('news:news_items', news_pk=items.pk)


def news_items(request, news_pk):
    items = get_object_or_404(News, pk=news_pk)
    comments = Comments.objects.filter(article=news_pk)
    best_comment = None
    for i in comments:
        if i.comment_like > 0:
            best_comment = comments.order_by('-comment_like').first()
    if request.method == 'POST':
        create_comment(request, items)
        return redirect('news:news_items', news_pk=items.pk)
    else:
        comment_form = CommentForm()
    context = {
        'items': items,
        'categories': category(),
        'comments': comments,
        'comment_form': comment_form,
        'best_comment': best_comment,
    }

    return render(request, 'news/news_items.html', context)


