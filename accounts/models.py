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
