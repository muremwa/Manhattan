from django.urls import path
from . import views

urlpatterns = [
    # /blog/
    path('', views.index, name="index"),

    # /blog/post4/
    path('post<int:id>/', views.post, name="post"),

    # /blog/author4/
    path('author<int:id>/', views.author, name="user"),

    # /blog/tags/
    path('tags/', views.tags, name="tags"),

    # /blog/tags/movies
    path('tags/<tag_name>/', views.tag, name="tag-detail"),

    # /blog/post4/comment
    path('post/comment/', views.comment, name="comment"),

]
