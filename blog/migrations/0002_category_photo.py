# Generated by Django 4.1.3 on 2022-11-14 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/blog/%Y/%m', verbose_name='Фото'),
        ),
    ]
