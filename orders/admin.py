from django.contrib import admin
from .models import Order, OrderItems


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    raw_id_fields = ['order_items']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
     '''Admin View for Order'''
     list_display = ['id',
                    'first_name',
                    'last_name', 
                    'email',
                    'city',
                    'address', 
                    'paid',
                    'created', 
                    'updated']

     list_filter = ['paid', 'created', 'updated']
     inlines = [OrderItemsInline]