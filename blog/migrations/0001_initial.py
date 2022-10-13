# Generated by Django 4.0.6 on 2022-10-12 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Назва категорії')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL')),
                ('content', models.TextField(blank=True, verbose_name='Вміст')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публікації')),
                ('photo', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d', verbose_name='Фото')),
                ('views', models.IntegerField(default=0, verbose_name='Перегляди')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='blog.category', verbose_name='Категорія')),
            ],
            options={
                'verbose_name': 'Стаття(ю)',
                'verbose_name_plural': 'Статті',
                'ordering': ['-created_at'],
            },
        ),
    ]
