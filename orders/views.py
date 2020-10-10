from django.shortcuts import render
from .models import Order, OrderItems
from cart.models import Cart, CartItem
from .forms import OrderForm
from django.contrib import messages



def create_order(request):
    cart = Cart.objects.get(user=request.user)
    user = cart.user
    total = cart.get_total()
    items = cart.items.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_form = form.save()
            for item in items:
                OrderItems.objects.create(user=user,
                                          order=order_form,
                                          order_items=item.item,
                                          price=item.item.price,
                                          quantity=item.quantity,
                                          total=total)
            #delete query set i.e cart
            items.delete()
            return render(request, 'orders/created.html',
                          {'order': order_form})
    else:
        form = OrderForm()
    return render(request, 'orders/create.html',
                  {'items': items, 'form': form, 'total': total})
