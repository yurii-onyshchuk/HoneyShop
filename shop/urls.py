from django.urls import path, include
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.Shop.as_view(), name='shop'),
    path('category/<str:slug>', views.ProductsByCategory.as_view(), name='category'),
    path('product/<str:slug>', views.DetailProduct.as_view(), name='product'),
    path('search/', views.Search.as_view(), name='search'),
    path('cart/', include('cart.urls'))
]
