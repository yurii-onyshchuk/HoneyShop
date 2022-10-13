from django.urls import path
from . import views

urlpatterns = [
    path('', views.Blog.as_view(), name='blog'),
    path('post/', views.SinglePost.as_view(), name='post'),
    path('category/<str:slug>', views.PostsByCategory.as_view(), name='category'),
    path('post/<str:slug>', views.SinglePost.as_view(), name='post'),
    path('search/', views.Search.as_view(), name='search'),
]
