from django.db import models
from django.conf import settings
from shop.models import Item


class Order(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)


    def __str__(self):
        return f'Order {self.id}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ('-created',)

class OrderItems(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order = models.ForeignKey(Order,
                              related_name='order',
                              on_delete=models.CASCADE)
    order_items = models.ForeignKey(Item,
                              related_name='order_items',
                              on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'OrderItems'
        verbose_name_plural = 'OrderItemss'

    def __str__(self):
        return str(self.id)
