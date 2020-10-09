from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from cart.models import Cart, CartItem
from django.contrib import messages

# Create your views here.


def create_order(request):
    pass