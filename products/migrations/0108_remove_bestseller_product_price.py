# Generated by Django 4.2.16 on 2024-10-31 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0107_remove_bestseller_product_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bestseller',
            name='product_price',
        ),
    ]
