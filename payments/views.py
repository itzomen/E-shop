from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from orders.models import Order, OrderItems
from cart.models import Coupon
# instantiate Braintree payment gateway
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe

stripe.api_key =settings.STRIPE_SECRET_KEY


@csrf_exempt
def payment_process(request):
    """
    payment process
    """
    order_id = request.session.get('order_id')
    
    order = get_object_or_404(Order, id=order_id)
    # converting order from decimal to interger
    order_total = int(order.total * 100)
    messages.info(request, f"Your Order total is {order.total}")

    if request.method == 'POST':
        domain_url = settings.DOMAIN_URL + 'payment/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                success_url=domain_url + 'success/',
                cancel_url=domain_url + 'cancelled/',
                
                
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': order_total,
                            'product_data': {
                                'name': f'Order Number {order.id}',
                                'images': ['https://i.imgur.com/EHyR2nP.png'],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment'
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    else:
        return render(request, 'payments/process.html',
                      {'order': order})


def payment_done(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    coupon_id = request.session.get('coupon_id')
    coupon = get_object_or_404(Coupon, id=coupon_id)

    order.coupon = coupon
    order.discount = coupon.discount
    order.paid = True
    order.save()
    return render(request, 'payments/paid.html')

def payment_canceled(request):
    return render(request, 'payments/cancelled.html')
