from django.apps import AppConfig


class ShopConfig(AppConfig):
    """Configuration class for the 'shop' app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'Магазин'
