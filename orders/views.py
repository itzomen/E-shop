from django.shortcuts import render
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from cart.models import Cart, CartItem
from shop.models import Item

# Create your views here.

class OrderCreateView(View):
    def create(self, *args, **kwargs):
        form = OrderForm(self.request.POST or None)
        try:
            cart = CartItem.objects.get(user=self.request.user, in_cart=True)
            if form.is_valid():
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=order
                                             item=cart.item
                                             quantity=cart.quantity
                                             price=cart.item.price
                                             cost=cart.quantity*cart.item.price)
                cart.clear()
                return render(self.request,
                              'orders/order/created.html',
                              {'order': order})
            
            else:
                form = OrderForm()
            return render(self.request,'orders/order/create.html',{'cart': cart, 'form': form})
 

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")