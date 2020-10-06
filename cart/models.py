from django.db import models
from django.conf import settings
from shop.models import Item

# Create your models here.
class CartItem(models.Model):
    """Model definition for CartItem."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    class Meta:
        """Meta definition for CartItem."""

        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'

    def __str__(self):
        """Unicode representation of CartItem."""
        return f"{self.quantity} of {self.item.name}"

    def get_total_price(self):
        return self.item.price * self.quantity

    def get_overall_price(self):
        return self.get_total_price()
