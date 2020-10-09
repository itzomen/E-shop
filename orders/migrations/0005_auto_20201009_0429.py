# Generated by Django 3.1.1 on 2020-10-09 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20201001_2112'),
        ('orders', '0004_remove_orderitem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='shop.item'),
        ),
    ]