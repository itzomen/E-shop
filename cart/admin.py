from django.contrib import admin
from .models import Cart, Coupon

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    '''Admin View for Cart'''

    list_display = ['user',
                    'added_date']
    list_filter = ['user', 'items', 'added_date']

    list_display_links = [
        'user',
        'added_date'
    ]
    search_fields = [
        'user'
    ]
    
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to',
                    'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
