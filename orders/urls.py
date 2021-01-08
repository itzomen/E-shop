from django.urls import path
from . import views
from .views import OrderView

app_name = 'orders'

urlpatterns = [
    path('order/', OrderView.as_view(), name='create-order'),
    path('admin/order/<int:order_id>/', views.admin_order_detail,
                                        name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, 
                                        name='admin_order_pdf'),
]