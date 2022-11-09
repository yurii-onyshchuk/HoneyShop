from django.urls import path
from . import views

urlpatterns = [
    path('', views.Checkout.as_view(), name='checkout'),
    path('payment/<int:pk>', views.payment, name='payment'),
    path('success/', views.CheckoutSuccess.as_view(), name='success'),
    path('payment-success/', views.PaymentSuccess.as_view(), name='payment_success'),
]
