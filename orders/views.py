from django.forms.forms import Form
from django.shortcuts import render, redirect
from .models import OrderItems
from cart.models import Cart
from .forms import OrderForm
from django.contrib import messages
from .tasks import email_order
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


def create_order(request):
    cart = Cart.objects.get(user=request.user)
    user = cart.user
    total = cart.get_total()
    items = cart.items.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
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
                request.session['order_id'] = order_form.id
                # redirect for payment
                messages.info(request, f"Your order was created")
                return redirect(reverse('payments:process'))
                # messages.info(request, f"Your order was created")
        else:
            messages.info(request, "Add items to cart")
            return redirect('cart:cart-summary')
    else:
        form = OrderForm()
    return render(request, 'orders/create.html',
                  {'items': items, 'form': form, 'total': total})
