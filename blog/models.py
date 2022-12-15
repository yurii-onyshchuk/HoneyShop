from django.db import models
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=250, verbose_name='Назва категорії')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)
    photo = models.ImageField(upload_to='photos/blog/%Y/%m', blank=True, verbose_name='Фото')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категорія статті'
        verbose_name_plural = 'Категорії статтей'
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категорія')
    content = models.TextField(blank=True, verbose_name='Вміст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публікації')
    photo = models.ImageField(upload_to='photos/blog/%Y/%m', blank=True, verbose_name='Фото')
    views = models.IntegerField(default=0, verbose_name='Перегляди')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slug': self.slug})

    def get_comment_count(self):
        return Comment.objects.filter(post=self, parent__isnull=True).count()

    class Meta:
        verbose_name = 'Стаття(ю)'
        verbose_name_plural = 'Статті'
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments', verbose_name='Пост')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET('Видалений користувач'),
                             related_name='user_comments', verbose_name='Користувач')
    body = models.TextField(verbose_name='Коментар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата додавання')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies',
                               verbose_name='До коментаря')
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_comments',
                                        verbose_name='Користувачі, які вподобали')

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ['-created_at']

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
