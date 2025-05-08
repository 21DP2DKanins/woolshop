# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('index/', views.index, name='index'),
    path('product_detail/', views.product_detail, name='product_detail'),
    path('collection/', views.collection, name='collection'),
    
]


