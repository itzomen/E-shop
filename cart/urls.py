from django.urls import path
from .views import add_to_cart, CartSummaryView

app_name = 'cart'

urlpatterns = [
    path('cart-summary/', CartSummaryView.as_view(), name='cart-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart')
]