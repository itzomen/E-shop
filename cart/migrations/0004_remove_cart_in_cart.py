# Generated by Django 3.1.1 on 2020-10-10 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20201008_2237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='in_cart',
        ),
    ]
