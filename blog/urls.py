from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # /blog/
    path('', views.index, name="index"),

    # /blog/post4/
    path('post<int:pk>/', views.post, name="post"),

    # /blog/new/post/
    path("new/post/", views.PostCreate.as_view(), name="create_post"),

    # /blog/edit/post24/
    path("edit/post<int:pk>/", views.PostEdit.as_view(), name="edit_post"),

    # /blog/edit/post24/delete
    path("edit/post<int:pk>/delete/", views.PostDelete.as_view(), name="delete_post"),

    # /blog/search
    path('search/', views.search, name="search"),

    # /blog/author4/
    path('author<int:pk>/', views.author, name="user"),

    # /blog/tags/
    path('tags/', views.TagsView.as_view(), name="tags"),

    # /blog/tags/movies
    path('tags/<tag_name>/', views.tag, name="tag-detail"),

    # /blog/ajax/comment
    path('ajax/comment/<int:post_id>/', views.comment, name="post_comment"),

]
