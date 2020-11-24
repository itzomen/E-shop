from django.contrib import admin
from .models import Order, OrderItems

import csv
import datetime
from django.http import HttpResponse


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    raw_id_fields = ['order_items']

def export_csv_file(modeladmin, request, queryset):
    options = modeladmin.model._meta
    content_disposition = f'attachment; filename={options.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [field for field in options.get_fields() if not field.many_to_many\
    and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_csv_file.short_description = 'Export Orders to CSV'


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
     actions = [export_csv_file]