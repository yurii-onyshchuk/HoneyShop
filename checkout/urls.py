from django.urls import path

from . import views

urlpatterns = [
    path('', views.Checkout.as_view(), name='checkout'),
    path('payment/<int:pk>', views.payment, name='payment'),
    path('callback/', views.callback, name='callback'),
    path('checkout-success/', views.CheckoutSuccess.as_view(), name='checkout_success'),
    path('payment-success/', views.PaymentSuccess.as_view(), name='payment_success'),
    path('payment-error/', views.PaymentError.as_view(), name='payment_error'),
    path('city_autocomplete/', views.city_autocomplete, name='city_autocomplete'),
]
