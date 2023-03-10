from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.conf import settings

import cloudipsp

from cart.cart import Cart
from checkout.forms import CheckoutForm
from checkout.utils import AllowOnlyRedirectMixin
from accounts.models import Address
from checkout.models import PaymentOptions
from order.models import Order, OrderItem
from shop.models import Product


class Checkout(LoginRequiredMixin, CreateView):
    extra_context = {'title': 'Оформлення замовлення'}
    template_name = 'checkout/checkout.html'
    model = Order
    form_class = CheckoutForm

    def get(self, request, *args, **kwargs):
        if not Cart(self.request):
            return redirect('order_list')
        return super().get(request, *args, **kwargs)

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
            order_item = OrderItem.objects.create(order_id=order.pk, product=item['product'], price=item['price'],
                                                  quantity=item['quantity'])
            product = Product.objects.get(id=item['product'].id)
            product.quantity = product.quantity - order_item.quantity
            product.save()
        cart.clear()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Виправте помилки в полях форми, що показані нижче! ')
        return super(Checkout, self).form_invalid(form)

    def get_success_url(self):
        method = PaymentOptions.objects.get(pk=int(self.request.POST.get('payment_option'))).method
        if method == 'AFTER':
            return reverse_lazy('checkout_success')
        elif method == 'ONLINE':
            self.object.refresh_from_db()
            return reverse_lazy('payment', kwargs={'pk': self.object.pk})


@login_required
def payment(request, pk):
    order = Order.objects.get(pk=pk)
    api = cloudipsp.Api(merchant_id=settings.FONDY_MERCHANT_ID, secret_key=settings.FONDY_CREDIT_KEY)
    checkout = cloudipsp.Checkout(api=api)
    data = {
        'order_desc': f'Замовленння №{order.id}',
        'amount': int(order.total_price * 100),
        'currency': 'UAH',
        'server_callback_url': request.build_absolute_uri(reverse_lazy('callback')),
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


def callback(request):
    if request.method == 'POST':
        data = request.POST
        api = cloudipsp.Api(merchant_id=settings.FONDY_MERCHANT_ID, secret_key=settings.FONDY_CREDIT_KEY)
        status = cloudipsp.Order(api).status(data)
        if status == 'approved':
            order = Order.objects.get(id=data['order_id'])
            order.billing_status = True
            order.save()
            return reverse_lazy('payment_success')
        else:
            return reverse_lazy('payment_error')
    else:
        return HttpResponseNotAllowed(['POST'])


class CheckoutSuccess(AllowOnlyRedirectMixin, LoginRequiredMixin, TemplateView):
    extra_context = {'title': 'Замовлення успішно оформлене'}
    template_name = 'checkout/checkout_success.html'
    allow_previous_url = reverse_lazy('checkout')
    redirect_url = reverse_lazy('order_list')


class PaymentSuccess(AllowOnlyRedirectMixin, LoginRequiredMixin, TemplateView):
    extra_context = {'title': 'Оплата успішна'}
    template_name = 'checkout/payment_success.html'
    redirect_url = reverse_lazy('order_list')


class PaymentError(AllowOnlyRedirectMixin, LoginRequiredMixin, TemplateView):
    extra_context = {'title': 'Помилка оплати'}
    template_name = 'checkout/payment_error.html'
    redirect_url = reverse_lazy('order_list')
