from django.db import models
from django.conf import settings
from cart.models import CartItem

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    created = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    order_info = models.ForeignKey(
        'OrderInfo', related_name='order_info', on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return f'Order {self.id}'

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class OrderInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'OrderInfos'