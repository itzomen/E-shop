from django.contrib import admin
from .models import CartItem, Cart

# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    '''Admin View for Cart'''

    list_display = ['user',
                    'added_date',
                    'ordered']
    list_filter = ['user', 'items', 'added_date']

    list_display_links = [
        'user',
        'added_date',
        'ordered'
    ]
    search_fields = [
        'user'
    ]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    '''Admin View for CartItem'''

    list_display = ['item', 'user']