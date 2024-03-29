from django.db import models


class DeliveryOptions(models.Model):
    """Model for defining delivery options.

    This model represents various methods of product delivery,
    including in-store pickup, delivery service pickup, and home delivery.
    """

    DELIVERY_CHOICES = [
        ("IN_STORE", "Самовивіз з магазину"),
        ("DELIVERY_SERVICE", "Самовивіз з служби доставки"),
        ("HOME_DELIVERY", "Кур'єр на вашу адресу"),
    ]

    title = models.CharField(verbose_name='Назва', max_length=255)
    price = models.CharField(verbose_name='Ціна', default='За тарифами перевізника', max_length=255)
    method = models.CharField(choices=DELIVERY_CHOICES, verbose_name="Метод доставки", max_length=255)
    is_active = models.BooleanField(verbose_name='Доступно', default=True)

    class Meta:
        verbose_name = 'Спосіб доставки'
        verbose_name_plural = 'Способи доставки'

    def __str__(self):
        return self.title


class PaymentOptions(models.Model):
    """Model for defining payment options.

    This model represents different methods of payment for orders,
    including payment upon receipt, online payment, and prepayment.
    """

    PAYMENT_CHOICES = [
        ("AFTER", "Оплата під час отримання товару"),
        ("ONLINE", "Онлайн оплата"),
        ("PREPAYMENT", "Передплата"),
    ]

    title = models.CharField(verbose_name='Назва', max_length=255)
    method = models.CharField(choices=PAYMENT_CHOICES, verbose_name="Метод оплати", max_length=255)
    is_active = models.BooleanField(verbose_name='Доступно', default=True)

    class Meta:
        verbose_name = 'Спосіб оплати'
        verbose_name_plural = 'Способи оплати'

    def __str__(self):
        return self.title
