import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order, OrderItems
# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    """
    payment process
    """
    order_id = request.session.get('order_id')
    order_total = request.session.get('order_total')
    order = get_object_or_404(Order, id=order_id)

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
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html',
                      {'order': order, 'client_token': client_token})