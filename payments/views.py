import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from orders.models import Order, OrderItems
# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    """
    payment process
    """
    order_id = request.session.get('order_id')
    orderitems_id = request.session.get('orderitems_id')

    order = get_object_or_404(Order, id=order_id)
    order_items = get_object_or_404(OrderItems, id=orderitems_id)
    order_total = order_items.total
    messages.info(request, f"{order_total} is total")

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale( {'amount': f'{order_total:.2f}',
                                            'payment_method_nonce': nonce,
                                            'options': {
                                            'submit_for_settlement': True}
                                            })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payments:done')
        else:
            return redirect('payments:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request, 'payments/process.html',
                      {'order': order, 'client_token': client_token})


def payment_done(request):
    return render(request, 'payments/done.html')

def payment_canceled(request):
    return render(request, 'payments/canceled.html')
