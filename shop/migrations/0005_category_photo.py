# Generated by Django 4.1.3 on 2022-11-14 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_product_users_wishlist_alter_review_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/shop/%Y/%m', verbose_name='Фото'),
        ),
    ]
