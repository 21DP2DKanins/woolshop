from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, 
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

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

def account(request):
    return render(request, 'shop/account.html')

def login(request):
    return render(request, 'shop/login.html')

def signup(request):
    return render(request, 'shop/signup.html')

def password_reset(request):
    return render(request, 'shop/password_reset.html')

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

from .forms import (
    SignUpForm, CustomLoginForm, CustomPasswordResetForm, 
    ProfileUpdateForm, PasswordChangeForm
)


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'
    
    def form_valid(self, form):
        remember = form.cleaned_data.get('remember', False)
        if not remember:
            # Если пользователь не выбрал "Запомнить меня", 
            # устанавливаем время жизни сессии до закрытия браузера
            self.request.session.set_expiry(0)
        
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = 'login'


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматически входим после регистрации
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('account')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


@login_required
def account_view(request):
    return render(request, 'account.html')


@login_required
def account_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('account')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'account.html', {'form': form})


@login_required
def account_change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Меняем пароль
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            # Обновляем сессию, чтобы пользователь не вылетел после смены пароля
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('account')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'account.html', {'password_form': form})


@login_required
def account_orders_view(request):
    # Здесь будет логика получения заказов пользователя
    orders = []  # Заглушка, в реальном проекте здесь будут заказы из БД
    return render(request, 'account_orders.html', {'orders': orders})


@login_required
def account_wishlist_view(request):
    # Здесь будет логика получения избранных товаров пользователя
    wishlist = []  # Заглушка, в реальном проекте здесь будут товары из БД
    return render(request, 'account_wishlist.html', {'wishlist': wishlist})


@login_required
def account_addresses_view(request):
    # Здесь будет логика получения адресов пользователя
    addresses = []  # Заглушка, в реальном проекте здесь будут адреса из БД
    return render(request, 'account_addresses.html', {'addresses': addresses})


@login_required
def account_settings_view(request):
    return render(request, 'account_settings.html')