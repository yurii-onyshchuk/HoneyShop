# Generated by Django 4.1.4 on 2023-03-10 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_user_managers_remove_user_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/accounts/%Y/%m', verbose_name='Основна світлина'),
        ),
    ]
