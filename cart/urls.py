from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add_to_cart/<int:item_id>', views.add_cart, name='add_cart'),
    path('reduce_from_cart/<int:item_id>', views.reduce_cart, name='reduce_cart'),
    path('remove_from_cart/<int:item_id>', views.remove_cart, name='remove_cart'),
]