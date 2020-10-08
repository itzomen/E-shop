from django.db import models
from django.conf import settings
from shop.models import Item

# Create your models here.
class CartItem(models.Model):
    """Model definition for CartItem."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    in_cart = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'

    def __str__(self):
        """Unicode representation of CartItem."""
        return f"{self.quantity} of {self.item.name}"

    def get_total_price(self):
        return self.item.price * self.quantity

    def item_final_price(self):
        return self.get_total_price()

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    added_date = models.DateTimeField(auto_now_add=True)
    in_cart = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        #calculate total price of items in cart
        for cart_item in self.items.all():
            total += cart_item.item_final_price()
        return total

    def count(self):
        #counting number of items in cart
        return len(self.items.all())
