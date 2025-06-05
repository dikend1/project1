from django.urls import path
from posts.views import post_list_create,post_detail,comment_created,like_create

urlpatterns = [
    path('',post_list_create,name='post_list_create'),
    path('<int:pk>',post_detail,name='post_detail'),
    path('<int:pk>/comment',comment_created,name='comment_create'),
    path('<int:pk>/like',like_create,name='like_create'),
]