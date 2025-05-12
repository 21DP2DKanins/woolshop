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
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('journal/', views.journal, name='journal'),
    path('account/', views.account, name='account'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Восстановление пароля
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Личный кабинет
    path('account/', views.account_view, name='account'),
    path('account/update/', views.account_update_view, name='account_update'),
    path('account/change-password/', views.account_change_password_view, name='account_change_password'),
    path('account/orders/', views.account_orders_view, name='account_orders'),
    path('account/wishlist/', views.account_wishlist_view, name='account_wishlist'),
    path('account/addresses/', views.account_addresses_view, name='account_addresses'),
    path('account/settings/', views.account_settings_view, name='account_settings'),
]
