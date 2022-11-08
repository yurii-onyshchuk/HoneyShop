from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from cart.cart import Cart
from .forms import CheckoutForm

from order.models import Order, OrderItem


class Checkout(LoginRequiredMixin, CreateView):
    extra_context = {'title': 'Оформлення замовлення'}
    template_name = 'checkout/checkout.html'
    model = Order
    form_class = CheckoutForm

    def form_valid(self, form):
        cart = Cart(self.request)
        form.instance.user = self.request.user
        form.instance.total_price = cart.get_total_price()
        order = form.save(commit=False)
        order.save()
        for item in cart:
            OrderItem.objects.create(order_id=order.pk, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()
        return super().form_valid(form)

    def get_success_url(self):
        if int(self.request.POST.get('payment_option')) == 1:
            return reverse_lazy('home')
        else:
            return reverse_lazy('home')
