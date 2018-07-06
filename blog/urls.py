from django.urls import path
from . import views

urlpatterns = [
    # /blog/
    path('', views.index, name="index"),

    # /blog/post/
    path('post<int:id>/', views.post, name="post"),

]
