from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Order


class OrderList(LoginRequiredMixin, ListView):
    extra_context = {'title': 'Мої замовлення'}
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
