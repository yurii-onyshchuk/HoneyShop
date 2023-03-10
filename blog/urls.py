from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostList.as_view(), name='blog'),
    path('category/<str:slug>', views.PostsByCategory.as_view(), name='category'),
    path('post/<str:slug>', views.SinglePost.as_view(), name='post'),
    path('search/', views.Search.as_view(), name='search'),
    path('like-comment/', views.like_comment, name='like_comment'),
]
