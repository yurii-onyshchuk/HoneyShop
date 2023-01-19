from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.conf import settings

import cloudipsp

from cart.cart import Cart
from checkout.forms import CheckoutForm
from order.models import Order, OrderItem
from checkout.models import PaymentOptions
from accounts.models import Address


class Checkout(LoginRequiredMixin, CreateView):
    extra_context = {'title': 'Оформлення замовлення'}
    template_name = 'checkout/checkout.html'
    model = Order
    form_class = CheckoutForm

    def get_initial(self):
        initial = super(Checkout, self).get_initial()
        initial = initial.copy()
        try:
            default_user_data = Address.objects.get(user=self.request.user, default_address=True)
            all_field = [field.name for field in Address._meta.get_fields()]
            for field in all_field:
                initial[field] = default_user_data.__getattribute__(field)
        except Address.DoesNotExist:
            pass
        finally:
            return initial

    def form_valid(self, form):
        cart = Cart(self.request)
        form.instance.user = self.request.user
        form.instance.total_price = cart.get_total_price()
        order = form.save(commit=False)
        order.save()
        for item in cart:
            OrderItem.objects.create(order_id=order.pk, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])
        return super().form_valid(form)

    def get_success_url(self):
        method = PaymentOptions.objects.get(pk=int(self.request.POST.get('payment_option'))).method
        if method == 'AFTER':
            cart = Cart(self.request)
            cart.clear()
            return reverse_lazy('success')
        elif method == 'ONLINE':
            self.object.refresh_from_db()
            return reverse_lazy('payment', kwargs={'pk': self.object.pk})


def payment(request, pk):
    order = Order.objects.get(pk=pk)
    api = cloudipsp.Api(merchant_id=settings.FONDY_MERCHANT_ID, secret_key=settings.FONDY_CREDIT_KEY)
    checkout = cloudipsp.Checkout(api=api)
    data = {
        'currency': 'UAH',
        'amount': int(order.total_price * 100),
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


class CheckoutSuccess(TemplateView):
    extra_context = {'title': 'Замовлення успішно оформлене'}
    template_name = 'checkout/checkout_success.html'


class PaymentSuccess(TemplateView):
    extra_context = {'title': 'Оплата успішна'}
    template_name = 'checkout/payment_success.html'
