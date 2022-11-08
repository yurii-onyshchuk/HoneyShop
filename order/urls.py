from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderList.as_view(), name='order_list'),
]
