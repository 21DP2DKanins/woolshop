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
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, PasswordResetRequestForm

import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, OrderItem, ProductVariant, Category
from .forms import OrderCreateForm

User = get_user_model()



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
    
    ],
    products = Product.objects.all().prefetch_related('variants').distinct()[:3]

    return render(request, 'shop/home.html', {
        'features': features,
        'now': timezone.now(),
        'products': products
    })

def index(request):
    products = Product.objects.all().prefetch_related('variants').distinct()
    return render(request, 'shop/index.html', {'products': products})



from django.shortcuts import render, get_object_or_404
from .models import Product

def collection(request):
    qs = Product.objects.all().prefetch_related('variants', 'category').distinct()


    category_slugs = request.GET.getlist('category')
    if category_slugs:
        qs = qs.filter(category__slug__in=category_slugs)

    color = request.GET.get('color')
    if color not in (None, '', 'None'):
        qs = qs.filter(variants__color=color)
    else:
        color = ''

    sizes = request.GET.getlist('size')
    if sizes:
        qs = qs.filter(variants__size__in=sizes)

    try:
        min_price = float(request.GET.get('min_price', 0))
        max_price = float(request.GET.get('max_price', 0))
        if min_price and max_price:
            qs = qs.filter(price__gte=min_price, price__lte=max_price)
    except (TypeError, ValueError):
        min_price = max_price = 0

    sort = request.GET.get('sort')
    if sort == 'price_low':
        qs = qs.order_by('price')
    elif sort == 'price_high':
        qs = qs.order_by('-price')
    elif sort == 'name_az':
        qs = qs.order_by('name')
    elif sort == 'name_za':
        qs = qs.order_by('-name')

    qs = qs.distinct()

    all_variants = ProductVariant.objects.filter(product__in=qs)
    available_colors = sorted(set(v.color for v in all_variants))
    available_sizes = sorted(set(v.size for v in all_variants))

    prices = qs.values_list('price', flat=True)
    price_min = int(min(prices)) if prices else 0
    price_max = int(max(prices)) if prices else 0

    return render(request, 'shop/collection.html', {
        'products': qs,
        'available_colors': available_colors,
        'available_sizes': available_sizes,
        'categories': Category.objects.all(),
        'price_min': price_min,
        'price_max': price_max,
        'selected': {
            'category': category_slugs,
            'color': color,
            'sizes': sizes,
            'min_price': min_price,
            'max_price': max_price,
            'sort': sort,
        }
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = list(product.variants.all())


    choice_map = dict(product.COLOR_CHOICES)
    available_colors = []
    for v in variants:
        code = v.color
        label = choice_map.get(code, code)
        if code not in [c for c, _ in available_colors]:
            available_colors.append((code, label))

    is_available = any(v.stock > 0 for v in variants)

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'variants': variants,
        'available_colors': available_colors,
        'is_available': is_available,
    })

def cart_view(request):
    # просто рендерим контейнер — всё рисует JS
    return render(request, 'shop/cart.html')


def contact(request):
    return render(request, 'shop/contact.html')

def about(request):
    return render(request, 'shop/about.html')

def journal(request):
    return render(request, 'shop/journal.html')

def account(request):
    return render(request, 'shop/account.html')

def login_view(request):
    return render(request, 'shop/login.html')

def signup(request):
    return render(request, 'shop/signup.html')

def password_reset(request):
    return render(request, 'shop/password_reset.html')


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
            self.request.session.set_expiry(0)
        
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = 'login'

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
            messages.success(request, 'Profile has been successfully updated!')
            return redirect('account')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'account.html', {'form': form})


@login_required
def account_change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('account')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'shop/account.html', {'password_form': form})


@login_required
def account_orders_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'shop/account_orders.html', {'orders': orders})



@login_required
def account_wishlist_view(request):
    
    wishlist = []  
    return render(request, 'account_wishlist.html', {'wishlist': wishlist})


@login_required
def account_addresses_view(request):
    
    addresses = []  
    return render(request, 'account_addresses.html', {'addresses': addresses})


@login_required
def account_settings_view(request):
    return render(request, 'account_settings.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            user.set_password(form.cleaned_data['password1'])
            user.newsletter = form.cleaned_data.get('newsletter', False)
            user.save()
            
            
            login(request, user)
            messages.success(request, _("Registration successful! Welcome to our shop."))
            return redirect('account')  
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'shop/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                
                
                if not remember_me:
                    request.session.set_expiry(0)  
                
                messages.success(request, _("You have been successfully logged in."))
                
                # Redirect to the page the user was trying to access, or home
                return redirect('home')
            else:
                messages.error(request, _("Invalid email or password."))
        else:
            messages.error(request, _("Invalid email or password."))
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'shop/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, _("You have been successfully logged out."))
    return redirect('home')


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(Q(email=email))
            
            if users.exists():
                user = users.first()
                current_site = get_current_site(request)
                subject = _("Password Reset Request")
                message = render_to_string("shop/password_reset_email.html", {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http',
                })
                
                try:
                    send_mail(subject, message, 'noreply@example.com', [user.email])
                    messages.success(request, _("Password reset email has been sent."))
                    return redirect('login')
                except BadHeaderError:
                    messages.error(request, _("An error occurred. Please try again later."))
                    return redirect('password_reset')
            else:
                messages.error(request, _("No user found with this email address."))
                return redirect('password_reset')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, "shop/password_reset.html", {"form": form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, _("Your password has been reset. You can now log in."))
                return redirect('login')
            else:
                for error in form.errors.values():
                    messages.error(request, error)
        else:
            form = SetPasswordForm(user)
        return render(request, 'shop/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, _("The password reset link is invalid or has expired."))
        return redirect('password_reset')
    


@login_required
def checkout_view(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        cart_json = request.POST.get('cart_json', '[]')

        try:
            cart = json.loads(cart_json)
        except json.JSONDecodeError:
            cart = []

        subtotal = sum(i.get('price', 0) * i.get('quantity', 1) for i in cart)
        total = subtotal

        if form.is_valid() and cart:
            order = form.save(commit=False)
            order.user = request.user
            order.paid = True

            # Сбор всех ошибок
            error_messages = []
            valid_variants = []

            for item in cart:
                variant_id = item.get('variantId')
                quantity = item.get('quantity', 1)

                variant = ProductVariant.objects.filter(id=variant_id).select_related('product').first()

                if not variant:
                    error_messages.append(f"Product variant not found (ID: {variant_id}).")
                    continue

                if quantity > variant.stock:
                    error_messages.append(
                        f'Not enough stock for {variant.product.name} ({variant.color}/{variant.size}). '
                        f'Only {variant.stock} left.'
                    )
                    continue

                valid_variants.append((item, variant))

            if error_messages:
                for msg in error_messages:
                    messages.error(request, msg)
                return redirect('checkout')

            # Всё ок — создаём заказ
            order.save()

            for item, variant in valid_variants:
                quantity = item.get('quantity', 1)
                OrderItem.objects.create(
                    order=order,
                    product_name=f"{variant.product.name} ({variant.color}/{variant.size})",
                    price=item.get('price'),
                    quantity=quantity
                )
                variant.stock = max(variant.stock - quantity, 0)
                variant.save()

            request.session.pop('cart', None)
            return render(request, 'shop/checkout_success.html', {'order': order})

    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}",
                'email': request.user.email,
            }

        form = OrderCreateForm(initial=initial_data)
        cart = json.loads(request.session.get('cart', '[]'))
        subtotal = sum(i.get('price', 0) * i.get('quantity', 1) for i in cart)
        total = subtotal

    return render(request, 'shop/checkout.html', {
        'form': form,
        'cart': cart,
        'totals': {'subtotal': subtotal, 'total': total},
    })


from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

@login_required
def account_reviews_view(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Your feedback has been sent!')
            return redirect('account_reviews')
    else:
        form = ReviewForm()

    return render(request, 'shop/account_reviews.html', {'form': form})

def journal(request):
    reviews = Review.objects.select_related('user').all()
    return render(request, 'shop/journal.html', {'reviews': reviews})

from django.contrib import messages
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been successfully sent. We will contact you shortly.")
            return redirect('contact')
        else:
            messages.error(request, "Check that the data entered is correct.")
    else:
        form = ContactForm()

    return render(request, 'shop/contact.html', {'form': form})

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')
    return redirect('account')