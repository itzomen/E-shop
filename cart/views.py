from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import AddItemForm

@require_POST
def add_cart(request, item_id):
    """
    this add item with the matching item_id to the cart
    """
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    form = AddItemForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add_item(item=item, quantity=cd['quantity'], 
                       override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def reduce_cart(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.reduce_item(item)
    return redirect('cart:cart_detail')

@require_POST
def remove_cart(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove_item(item)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
