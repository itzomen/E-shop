from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
 model = OrderItem
 raw_id_fields = ['item']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''

    list_display = [
        'id',
        'user',
        'email',
        'city',
        'address',
        'ordered',
        'created',
        'updated',
        'paid' 
    ]

    list_display_links = [
        'id',
        'user',
        'ordered',
        'created',
        'updated',
        'paid'
    ]
    
    list_filter = [
        'id',
        'user',
        'ordered',
        'created',
        'paid',
        'updated']

    search_fields = [
        'id',
        'user__username',
        'first_name',
        'last_name'
    ]
    inlines = [OrderItemInline]