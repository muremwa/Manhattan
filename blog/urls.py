from django.urls import path
from . import views

urlpatterns = [
    # /blog/
    path('', views.index, name="index"),

    # /blog/post4/
    path('post<int:id>/', views.post, name="post"),


    # /blog/search
    path('search/', views.search, name="search"),

    # /blog/author4/
    path('author<int:id>/', views.author, name="user"),

    # /blog/tags/
    path('tags/', views.tags, name="tags"),

    # /blog/tags/movies
    path('tags/<tag_name>/', views.tag, name="tag-detail"),

    # /blog/ajax/comment
    path('ajax/comment/', views.comment, name="post_comment"),

    # /blog/ajax/comments
    path('ajax/comments/', views.all_comments, name="all-comments"),

]
