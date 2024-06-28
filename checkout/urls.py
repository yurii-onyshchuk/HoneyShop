from django.urls import path

from . import views

urlpatterns = [
    path('', views.Checkout.as_view(), name='checkout'),
    path('payment/<int:pk>', views.payment, name='payment'),
    path('checkout-success/', views.CheckoutSuccess.as_view(), name='checkout_success'),
    path('payment-response/', views.payment_response, name='payment_response'),
    path('payment-success/', views.PaymentSuccess.as_view(), name='payment_success'),
    path('payment-error/', views.PaymentError.as_view(), name='payment_error'),
]
