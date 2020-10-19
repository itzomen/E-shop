from django.shortcuts import render, redirect
from .models import Order, OrderItems
from cart.models import Cart, CartItem
from .forms import OrderForm
from django.contrib import messages
from .tasks import email_order
#used payments app
from django.urls import reverse



def create_order(request):
    cart = Cart.objects.get(user=request.user)
    user = cart.user
    total = cart.get_total()
    items = cart.items.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if items:
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
                # delay to launch the task asynchronously
                email_order.delay(order_form.id)
                # set the order in the session
                request.user['order_id'] = order_form.id
                # redirect for payment
                return redirect(reverse('payment:process'))
                # messages.info(request, f"Your order was created")
                # return render(request, 'orders/created.html',
                #             {'order': order_form})
        else:
            messages.info(request, "Add items to cart")
            return redirect('cart:cart-summary')
    else:
        form = OrderForm()
    return render(request, 'orders/create.html',
                  {'items': items, 'form': form, 'total': total})
