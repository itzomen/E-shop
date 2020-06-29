from django.contrib import admin
from .models import Category, Item

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Item)
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for Item'''

    list_display = ['name', 'slug', 'price',
                    'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'created', 'updated']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('name',)}
