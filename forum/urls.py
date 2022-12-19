from django.urls import path
from forum.views import category_list, topic_detail, topic_list, topic_filter_new, \
    topic_filter_takepart, complain


app_name = 'forum'

urlpatterns = [
    path('', category_list, name='category_list'),
    path('topic_list/<int:detail_pk>/', topic_list, name='topic_list'),
    path('topic/<int:topic_pk>/', topic_detail, name='topic_detail'),
    path('topic_filter_new/', topic_filter_new, name='topic_filter_new'),
    path('topic_filter_takepart/', topic_filter_takepart, name='topic_filter_takepart'),
    path('<int:post_pk>/complain/', complain, name='complain'),
]
