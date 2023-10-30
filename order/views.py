from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Order


class OrderList(LoginRequiredMixin, ListView):
    """View for displaying a list of user's orders.

    This view displays a paginated list of orders associated
    with the logged-in user.
    """

    extra_context = {'title': 'Мої замовлення',
                     'subtitle': 'Переглядайте, відстежуйте, змінюйте або купуйте знову'}
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        """Get the queryset of orders for the logged-in user."""
        return Order.objects.filter(user=self.request.user)
