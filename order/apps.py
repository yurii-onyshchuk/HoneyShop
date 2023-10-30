from django.apps import AppConfig


class OrderConfig(AppConfig):
    """Configuration class for the 'order' app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order'
    verbose_name = 'Замовлення'