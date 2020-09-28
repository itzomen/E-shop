from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.item_list, name='item_list'),
path('', views.all_items, name='all_items'),
    path('<slug:category_slug>/', views.item_list, name='item_list_by_category'),
    path('<int:id>/<slug:slug>/', views.item_detail, name='item_detail'),
]