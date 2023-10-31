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
from checkout.mixins import AllowOnlyRedirectMixin
from accounts.models import Address
from checkout.models import PaymentOptions
from order.models import Order, OrderItem
from shop.models import Product


class Checkout(LoginRequiredMixin, CreateView):
    """View for processing and handling the order checkout.

    This view is responsible for processing the order checkout,
    collecting user input, and creating a new order.
    """

    extra_context = {'title': 'Оформлення замовлення'}
    template_name = 'checkout/checkout.html'
    model = Order
    form_class = CheckoutForm

    def get(self, request, *args, **kwargs):
        """Handle the GET request for order checkout.
        Redirects to 'order_list' if the cart is empty.
        """
        if not Cart(self.request):
            return redirect('order_list')
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        """Initialize the checkout form with default user data.
        Retrieves the default user data, if available, and initializes the form fields.
        """
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
        """Handle a valid form submission.
        Creates a new order, updates product quantities, and clears the cart.
        """
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
        """Handle an invalid form submission.
        Displays an error message if the form contains errors.
        """
        messages.error(self.request, 'Виправте помилки в полях форми, що показані нижче! ')
        return super(Checkout, self).form_invalid(form)

    def get_success_url(self):
        """Determine the success URL based on the selected payment method.
        Returns the success URL based on the payment method chosen in the form.
        """
        method = PaymentOptions.objects.get(pk=int(self.request.POST.get('payment_option'))).method
        if method == 'AFTER':
            return reverse_lazy('checkout_success')
        elif method == 'ONLINE':
            self.object.refresh_from_db()
            return reverse_lazy('payment', kwargs={'pk': self.object.pk})


@login_required
def payment(request, pk):
    """View for handling payment processing and redirection.

    This view processes payments and redirects the user to
    the payment gateway.
    """
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
    """Callback view for processing payment gateway responses.

    This view handles the response from the payment gateway
    and updates the order status accordingly.
    """
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
    """View to display a successful order checkout message.

    This view displays a success message after a successful
    order checkout.
    """

    extra_context = {'title': 'Замовлення успішно оформлене'}
    template_name = 'checkout/checkout_success.html'
    allow_previous_url = reverse_lazy('checkout')
    redirect_url = reverse_lazy('order_list')


class PaymentSuccess(AllowOnlyRedirectMixin, LoginRequiredMixin, TemplateView):
    """View to display a successful payment message.

    This view displays a success message after a successful
    payment.
    """

    extra_context = {'title': 'Оплата успішна'}
    template_name = 'checkout/payment_success.html'
    redirect_url = reverse_lazy('order_list')


class PaymentError(AllowOnlyRedirectMixin, LoginRequiredMixin, TemplateView):
    """View to display an error message for payment.

    This view displays an error message when there's
    an issue with the payment.
    """

    extra_context = {'title': 'Помилка оплати'}
    template_name = 'checkout/payment_error.html'
    redirect_url = reverse_lazy('order_list')
