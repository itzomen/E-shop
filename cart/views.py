from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from shop.models import Item
from .models import Cart, CartItem
from django.utils import timezone
from django.contrib import messages


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart_item, created = CartItem.objects.get_or_create( 
                            item=item,
                            user=request.user,
                            ordered=False)
    cart_qs = Cart.objects.filter(user=request.user, ordered=False)
    if cart_qs.exists():
        cart = cart_qs[0]
        # checking if item in cart
        if cart.items.filter(item__slug=item.slug).exists():
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, f"{item.name} quantity was increased.")
            return redirect('cart:cart-summary')
        else:
            cart.items.add(cart_item)
            messages.info(request, f"{item.name} was added to your cart.")
            return redirect('cart:cart-summary')
    else:
        added_date = timezone.now()
        cart = Cart.objects.create(user=request.user, added_date=added_date)
        cart.items.add(cart_item)
        messages.info(request, f"{item.name} was added to your cart.")
        return redirect('cart:cart-summary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart_qs = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the item is in the cart
        if cart.items.filter(item__slug=item.slug).exists():
            cart_item = CartItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            cart.items.remove(cart_item)
            cart_item.delete()
            messages.info(request, f"{item.name} was removed from your cart.")
            return redirect('cart:cart-summary')
        else:
            messages.info(request, f"{item.name} was not in your cart")
            return render(request, 'shop/item/item.html', 
                            {'item': item})
    else:
        messages.info(request, "You have item in your cart")
        return render(request, 'shop/item/item.html', 
                            {'item': item})



@login_required
def reduce_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart_qs = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the item is in the cart
        if cart.items.filter(item__slug=item.slug).exists():
            cart_item = CartItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart.items.remove(cart_item)
            messages.info(request, f"{item.name} quantity was reduced from your cart.")
            return redirect('cart:cart-summary')
        else:
            messages.info(request, "This item was not in your cart")
            return render(request, 'shop/item/item.html', 
                            {'item': item})
    else:
        messages.info(request, "You do not have an active order")
        return render(request, 'shop/item/item.html', 
                            {'item': item})



class CartSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': cart
            }
            return render(self.request, 'cart/cart_detail.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")