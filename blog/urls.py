from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('post/', views.post, name='post'),
    path('follow/', views.follow, name='follow'),
    path('unfollow/', views.unfollow, name='unfollow'),
]