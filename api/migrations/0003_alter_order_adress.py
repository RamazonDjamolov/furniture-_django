# Generated by Django 5.0.2 on 2024-02-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_order_adress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='adress',
            field=models.CharField(max_length=100),
        ),
    ]
