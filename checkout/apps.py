from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """Configuration class for the "checkout" app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'
    verbose_name = 'Оформлення замовлення'
