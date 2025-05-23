# shop/urls.py
from django.urls import path, include
from . import views
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin



urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),

    path('collection/', views.collection, name='collection'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),

    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('journal/', views.journal, name='journal'),
    path('account/', views.account, name='account'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout_view, name='checkout'),

    
    
    
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
    path('account/reviews/', views.account_reviews_view, name='account_reviews'),
    path('account/delete/', views.delete_account_view, name='account_delete'),


    # Password reset URLs
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='shop/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='shop/password_reset_complete.html'
    ), name='password_reset_complete'),
]
