from django.urls import path
from news.views import news_list, news_in_category, news_items, like_or_dislike

app_name = 'news'

urlpatterns = [
    path('', news_list, name='news_list'),
    path('<int:news_pk>/', news_items, name='news_items'),
    path('<int:news_pk>/<int:comment_pk>/<str:vote>', like_or_dislike, name='like_or_dislike'),
    path('<slug>/', news_in_category, name='news_in_category'),
]
