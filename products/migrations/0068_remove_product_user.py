# Generated by Django 4.0.10 on 2024-07-10 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0067_product_artikul'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
    ]
