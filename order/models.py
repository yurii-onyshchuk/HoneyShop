from django.conf import settings
from django.db import models
from phonenumber_field import modelfields

from shop.models import Product
from checkout.models import DeliveryOptions, PaymentOptions


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Користувач')
    recipient_first_name = models.CharField(verbose_name="Ім'я отримувача", max_length=100)
    recipient_last_name = models.CharField(verbose_name="Прізвище отримувача", max_length=100)
    recipient_patronymic = models.CharField(verbose_name="По-батькові отримувача", max_length=100)
    recipient_phone_number = modelfields.PhoneNumberField(verbose_name='Номер телефону отримувача')
    delivery_option = models.ForeignKey(DeliveryOptions, on_delete=models.CASCADE, verbose_name="Спосіб доставки")
    city = models.CharField(verbose_name='Місто', max_length=50, blank=True, null=True)
    street = models.CharField(verbose_name='Вулиця', max_length=50, blank=True, null=True)
    house = models.CharField(verbose_name='Будинок', max_length=6, blank=True, null=True)
    flat = models.CharField(verbose_name='Квартира', max_length=5, blank=True, null=True)
    delivery_service_department = models.CharField(verbose_name='Відділення служби доставки', max_length=50, blank=True, null=True)
    payment_option = models.ForeignKey(PaymentOptions, verbose_name='Спосіб оплати', on_delete=models.CASCADE)
    billing_status = models.BooleanField(verbose_name='Здійснено оплату', default=False)
    total_price = models.DecimalField(verbose_name='Загальна сума оплати', max_digits=7, decimal_places=0)
    created_at = models.DateTimeField(verbose_name='Дата додавання', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата оновлення', auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return f'Замовлення №{str(self.pk)}'

    def get_recipient(self):
        return f'{self.recipient_last_name} {self.recipient_first_name} {self.recipient_patronymic}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Замовлення')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(max_digits=7, decimal_places=0, verbose_name='Вартість')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')

    class Meta:
        verbose_name = 'Позиція замовлення'
        verbose_name_plural = 'Позиції замовлення'

    def __str__(self):
        return f'№{str(self.pk)} (замовлення №{str(self.order.pk)})'

    def total_price(self):
        return self.quantity * self.price
