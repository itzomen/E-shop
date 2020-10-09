from django.db import models
from django.conf import settings
from shop.models import Item

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
  
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    order_cost = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order =  models.ForeignKey(Order, 
                              related_name='order', 
                              on_delete=models.CASCADE)
    item = models.ForeignKey(Item, 
                              related_name='item', 
                              on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems'

    def __str__(self):
        return str(self.id)