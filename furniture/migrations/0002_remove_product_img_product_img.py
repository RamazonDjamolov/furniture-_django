# Generated by Django 5.0.2 on 2024-03-05 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furniture', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='img',
        ),
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.ManyToManyField(to='furniture.img', verbose_name='product_img'),
        ),
    ]
