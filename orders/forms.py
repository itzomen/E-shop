from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    """Form definition for Order."""

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 
                'email', 'city', 'address',
                'postal_code']

