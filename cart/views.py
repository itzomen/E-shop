from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Item
from .cart import Cart
from django.contrib import messages
