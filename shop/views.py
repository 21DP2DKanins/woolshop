from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.utils import timezone


# Create your views here.
def home(request):
    features = [
    {
        'icon': '<i class="fas fa-cog"></i>',
        'title': 'Настройка',
        'text': 'Легко настраивайте свой проект под любые нужды.'
    },
    {
        'icon': '<i class="fas fa-shield-alt"></i>',
        'title': 'Безопасность',
        'text': 'Надёжная защита данных ваших пользователей.'
    },
    {
        'icon': '<i class="fas fa-rocket"></i>',
        'title': 'Производительность',
        'text': 'Высокая скорость и масштабируемость.'
    },
    # добавьте столько элементов, сколько нужно
    ],
    products = Product.objects.all()

    return render(request, 'shop/home.html', {
        'features': features,
        'now': timezone.now(),
        'products': products
    })

def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

def product_detail(request):
    return render(request, 'shop/product_detail.html')

def collection(request):
    products = Product.objects.all()
    return render(request, 'shop/collection.html', {'products': products})

def contact(request):
    return render(request, 'shop/contact.html')

def about(request):
    return render(request, 'shop/about.html')

def journal(request):
    return render(request, 'shop/journal.html')

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