from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Item
from .models import CartItem
from django.contrib import messages


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart_item, created = CartItem.objects.get_or_create( 
                            item=Item,
                            user=request.user,
                            ordered=False)
    cart_qs = CartItem.objects.filter(user=request.user, ordered=False)
    if cart_qs.exists():
        cart = cart_qs[0]
        # checking if item in cart
        if cart.items.filter(item__slug=item.slug).exists():
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, f"{item.name} quantity was increased.")
            return redirect('cart:cart_detail')
        else:
            cart.tems.add(cart_item)
            messages.info(request, f"{item.name} was added to your cart.")
            return redirect('cart:cart_detail')
    else:
        cart = CartItem.objects.create(user=request.user)
        cart.items.add(cart_item)
        messages.info(request, f"{item.name} was added to your cart.")
        return redirect('cart:cart_detail')