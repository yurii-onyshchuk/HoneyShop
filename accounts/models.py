from django.db import models
from phonenumber_field import modelfields
from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    slug = AutoSlugField(populate_from='username', verbose_name='URL', unique=True)
    phone_number = modelfields.PhoneNumberField(null=False, blank=False, unique=True, verbose_name='Номер телефону')
    photo = models.ImageField(upload_to='photos/accounts/%Y/%m', blank=True, verbose_name='Основна світлина')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата народження')

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return str(self.username)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')
    recipient_first_name = models.CharField(verbose_name="Ім'я отримувача", max_length=100)
    recipient_last_name = models.CharField(verbose_name="Прізвище отримувача", max_length=100)
    recipient_patronymic = models.CharField(verbose_name="По-батькові отримувача", max_length=100)
    recipient_phone_number = modelfields.PhoneNumberField(verbose_name='Номер телефону отримувача')
    city = models.CharField(verbose_name='Місто', max_length=50)
    street = models.CharField(verbose_name='Вулиця', max_length=50)
    house = models.CharField(verbose_name='Будинок', max_length=6)
    flat = models.CharField(verbose_name='Квартира', max_length=5, blank=True)
    created_at = models.DateTimeField(verbose_name='Дата додавання', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата оновлення', auto_now=True)
    default_address = models.BooleanField(verbose_name='За замовчуванням', default=False)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреси"
        ordering = ['-default_address']

    def __str__(self):
        return f'{self.recipient_first_name} {self.recipient_last_name}'
