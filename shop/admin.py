
# shop/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import (
    Product,
    Profile,
    CustomUser,
    Order,
    OrderItem
)

# --- Регистрация модели CustomUser ---
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    filter_horizontal = ('groups', 'user_permissions',)

# --- Регистрация модели Product ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'color', 'size', 'created_at')
    list_filter = ('color', 'size', 'created_at')
    search_fields = ('name', 'description')

# --- Регистрация модели Profile ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date', 'newsletter')
    search_fields = ('user__email', 'phone')
    list_filter = ('newsletter',)

# --- Inline для OrderItem в Order ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# --- Регистрация модели Order ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'city', 'created_at', 'paid')
    list_filter = ('paid', 'created_at')
    search_fields = ('full_name', 'email', 'address', 'city')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)

# --- Регистрация модели OrderItem ---
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'price', 'quantity')
    search_fields = ('product_name', 'order__id')

# Отменяем регистрацию стандартного пользователя и регистрируем CustomUser
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass
admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from .models import ContactMessage
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'message')
    search_fields = ('first_name', 'last_name', 'email', 'message')
