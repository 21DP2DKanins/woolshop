from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.utils import timezone


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})

def index(request):
    return render(request, 'shop/index.html')

def product_detail(request):
    return render(request, 'shop/product_detail.html')

def collection(request):
    products = Product.objects.all()
    return render(request, 'shop/collection.html', {'products': products})

def add_to_cart(request, product_id):
    """
    Добавляет товар в корзину (хранится в сессии) 
    и перенаправляет на страницу корзины.
    """
    # Получаем текущее состояние корзины из сессии или пустой словарь
    cart = request.session.get('cart', {})

    # Увеличиваем количество для этого product_id
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    # Сохраняем обновлённую корзину в сессии
    request.session['cart'] = cart

    return redirect('cart')


def cart_view(request):
    """
    Отображает содержимое корзины: товары, их количество и сумму.
    """
    cart = request.session.get('cart', {})
    # Получаем объекты Product по ключам из корзины
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0
    for product in products:
        qty = cart.get(str(product.id), 0)
        item_total = product.price * qty
        total += item_total
        cart_items.append({
            'product': product,
            'quantity': qty,
            'item_total': item_total,
        })

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })