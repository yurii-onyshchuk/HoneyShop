from django.db import models
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Назва категорії товару')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категорія товару'
        verbose_name_plural = 'Категорії товарів'
        ordering = ['title']


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='Категорія')
    title = models.CharField(max_length=250, verbose_name='Назва')
    slug = models.SlugField(max_length=250, verbose_name='URL', unique=True)
    photo = models.ImageField(upload_to='photos/shop/%Y/%m', blank=True, verbose_name='Фото')
    description = models.TextField(blank=True, verbose_name='Опис')
    price = models.DecimalField(verbose_name='Ціна', max_digits=7, decimal_places=0)
    available = models.DecimalField(default=0, verbose_name='Доступно', max_digits=7, decimal_places=2)
    sales = models.IntegerField(default=0, verbose_name='Продажі')
    views = models.IntegerField(default=0, verbose_name='Перегляди')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата додавання')
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True,
                                            verbose_name='Користувачі, що вподобали')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product', kwargs={'slug': self.slug})

    def get_reviews_count(self):
        return Review.objects.filter(product=self, parent__isnull=True).count()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['-available']


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET('Видалений користувач'),
                             related_name='reviews', verbose_name='Користувач')
    body = models.TextField(verbose_name='Коментар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата додавання')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies',
                               verbose_name='До коментаря')

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ['-created_at']

    @property
    def children(self):
        return Review.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
