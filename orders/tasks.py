from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def email_order(order_id):
    """
    This task sends the order number via email to the user
    upon successful order
    """
    order = Order.objects.get(id=order_id)
    subject = f'E-shop Order Number {order.id}'
    message = f'Dear {order.first_name},\n\n' \
    f'You have successfully ordered from E-shop.' \
    f'Your order ID is {order.id}.'
    e_mail = send_mail(subject,
                       message,
                       'admin@E-shop.com',
                       [order.email])
    return e_mail