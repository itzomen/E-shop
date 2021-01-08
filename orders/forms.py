from django import forms
from .models import Order
#from cart.models import Coupon

class OrderForm(forms.ModelForm):
    """Form definition for Order."""

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 
                'email', 'city', 'address']

class CouponForm(forms.Form):
    code = forms.CharField(label=('Coupon'))
