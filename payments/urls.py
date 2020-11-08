from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('success/', views.payment_done, name='success'),
    path('cancelled/', views.payment_canceled, name='cancelled'),
]