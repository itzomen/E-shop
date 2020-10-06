from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Category, Item

# Create your views here.

def item_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    items = Item.objects.filter(in_stock=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        items = items.filter(category=category)
    return render(request, 'shop/item/store_items.html',
                 {'category': category,
                 'categories': categories,
                 'items': items})

class AllView(ListView):
    model = Item
    paginate_by = 2
    template_name = "shop/item/all_items.html"

def item_detail(request, id, slug):
    item = get_object_or_404(Item, id=id, slug=slug, in_stock=True)
    return render(request, 'shop/item/item.html', 
                            {'item': item})
    # the slug parameter is added to make seo-friendly urls
    
    
    
        
    
