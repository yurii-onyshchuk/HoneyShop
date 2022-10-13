from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=250, verbose_name='Назва категорії')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категорія')
    content = models.TextField(blank=True, verbose_name='Вміст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публікації')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, verbose_name='Фото')
    views = models.IntegerField(default=0, verbose_name='Перегляди')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Стаття(ю)'
        verbose_name_plural = 'Статті'
        ordering = ['-created_at']
