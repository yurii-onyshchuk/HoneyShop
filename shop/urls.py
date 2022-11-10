from django.urls import path, include
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.Shop.as_view(), name='shop'),
    path('category/<str:slug>', views.ProductsByCategory.as_view(), name='category'),
    path('product/<str:slug>', views.DetailProduct.as_view(), name='product'),
    path('search/', views.Search.as_view(), name='search'),
    path('wishlist/', views.WishListView.as_view(), name='wishlist'),
    path('to-wishlist/', views.add_or_remove_to_wishlist, name='add_or_remove_to_wishlist'),
    path('wishlist/clear/', views.clear_wishlist, name='clear_wishlist'),
    path('cart/', include('cart.urls'))
]
