from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('cart_add/', views.cart_add, name='cart_add'),
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('delete/<int:product_id>/', views.cart_delete, name='cart_delete'),
    path('clear/', views.clear_cart, name='clear_cart'),
]
