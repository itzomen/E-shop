from django.contrib import admin
from .models import Order, OrderInfo

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'items',
                    'created',
                    'ordered',
                    'paid'
                    ]
    list_display_links = [
        'user',
        'order_info'
    ]
    list_filter = ['ordered',
                   'paid']

    search_fields = [
        'user__username',
        'ordered'
    ]


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'first_name',
        'last_name',
        'email',
        'city',
        'address'
    ]
    list_filter = ['user', 'first_name']
    search_fields = ['user']


admin.site.register(OrderInfo, OrderInfoAdmin)