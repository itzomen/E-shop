from django.forms.forms import Form
from django.shortcuts import render, redirect
from .models import OrderItems
from cart.models import Cart, Coupon
from .forms import OrderForm, CouponForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from .tasks import email_order
from django.utils import timezone
#used payments app
from django.urls import reverse
#added for custom admin views
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
#used to generate pdf
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/admin/order_detail.html',
                            {'order': order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response


class OrderView(View):
    def get(self, *args, **kwargs):
        
        cart = Cart.objects.get(user=self.request.user)
        total = cart.get_total()
        items = cart.items.all()
        form = OrderForm()
        coupon_form = CouponForm()
        context = {
            'form': form,
            'coupon_form': coupon_form,
            'items': items,
            'total': total,
        }
        return render(self.request, 'orders/create.html', context)

    def post(self, *args, **kwargs):

        cart = Cart.objects.get(user=self.request.user)
        user = cart.user
        total = cart.get_total()
        items = cart.items.all()

        form = OrderForm(self.request.POST or None)
        if items:
            if form.is_valid():
                order_form = form.save(commit=False)
                order_form.total = total
                order_form.save()
                for item in items:
                    orderitems = OrderItems.objects.create(user=user,
                                            order=order_form,
                                            order_items=item.item,
                                            price=item.item.price,
                                            quantity=item.quantity)
                #delete query set i.e cart
                items.delete()
                # delay to launch the task asynchronously
                email_order.delay(order_form.id)
                # set the order and orderitems id in session
                self.request.session['order_id'] = order_form.id
                # redirect for payment
                messages.info(self.request, f"Your order was created")
                return redirect(reverse('payments:process'))
                # messages.info(request, f"Your order was created")
        else:
            messages.info(self.request, "Add items to cart")
            return redirect('cart:cart-summary')

def get_coupon(request, code):
    now = timezone.now()
    try:
        coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
        return coupon
    except Coupon.DoesNotExist:
        messages.info(request, "This coupon does not exist")

class AddCouponView(View):
    def post(self, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user)

        coupon_form = CouponForm(self.request.POST or None)
        if coupon_form.is_valid():
            code = coupon_form.cleaned_data['code']
            cart.coupon = get_coupon(self.request, code)               
            if cart.coupon:
                cart.discount = cart.coupon.discount
                cart.save()
                self.request.session['coupon_id'] = cart.coupon.id
                messages.success(self.request, "Successfully added coupon")
                messages.info(self.request, f"{cart.coupon.discount}% OFF Coupon")
            
            return redirect('orders:create-order')
           