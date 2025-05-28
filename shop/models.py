from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Product
class Product(models.Model):
    name        = models.CharField(max_length=200, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    price       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price, ₽")
    image       = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True, verbose_name="Image")
    stock       = models.PositiveIntegerField(default=0, verbose_name="Stock")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at  = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    # --- new fields ---
    COLOR_CHOICES = [
        ('red',   'Red'),
        ('green', 'Green'),
        ('blue',  'Blue'),
        ('black', 'Black')
        ('orange', 'Orange')
        # extend if needed
    ]
    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default='red',
        verbose_name="Color"
    )

    SIZE_CHOICES = [
        ('S',  'S'),
        ('M',  'M'),
        ('L',  'L'),
        ('XL', 'XL'),
        # extend if needed
    ]
    size = models.CharField(
        max_length=5,
        choices=SIZE_CHOICES,
        default='M',
        verbose_name="Size"
    )
    # -----------------

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    size = models.CharField(max_length=5, choices=Product.SIZE_CHOICES)
    color = models.CharField(max_length=20, choices=Product.COLOR_CHOICES)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} – {self.color} / {self.size}"


# User Profile
class Profile(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone       = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone")
    birth_date  = models.DateField(blank=True, null=True, verbose_name="Birth date")
    newsletter  = models.BooleanField(default=False, verbose_name="Newsletter subscription")

    def __str__(self):
        return f"{self.user.email} — profile"


# Signals for Profile
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Manager for custom user
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields['is_staff']:
            raise ValueError('Superuser must have is_staff=True')
        if not extra_fields['is_superuser']:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


# Custom User model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email        = models.EmailField('Email', unique=True)
    first_name   = models.CharField('First name', max_length=30, blank=True)
    last_name    = models.CharField('Last name', max_length=30, blank=True)
    phone        = models.CharField('Phone', max_length=20, blank=True, null=True)
    is_staff     = models.BooleanField('Staff status', default=False)
    is_active    = models.BooleanField('Active', default=True)
    date_joined  = models.DateTimeField('Date joined', default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class Order(models.Model):
    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="User"
    )
    full_name   = models.CharField("Full name", max_length=200)
    email       = models.EmailField("Email")
    address     = models.CharField("Address", max_length=300)
    city        = models.CharField("City", max_length=100)
    postal_code = models.CharField("Postal code", max_length=20)
    created_at  = models.DateTimeField("Created at", auto_now_add=True)
    paid        = models.BooleanField("Paid", default=False)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order {self.id} by {self.full_name}"
    
    def get_total_price(self):
        return sum(item.quantity * item.price for item in self.items.all())


class OrderItem(models.Model):
    order        = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product_name = models.CharField("Product name", max_length=200)
    price        = models.DecimalField("Price per item", max_digits=10, decimal_places=2)
    quantity     = models.PositiveIntegerField("Quantity")

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.quantity} × {self.product_name}"


class Review(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    content     = models.TextField("Review")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"Review by {self.user.email}"


class ContactMessage(models.Model):
    first_name  = models.CharField("First name", max_length=50)
    last_name   = models.CharField("Last name", max_length=50)
    email       = models.EmailField("Email")
    phone       = models.CharField("Phone", max_length=20, blank=True)
    message     = models.TextField("Message")
    created_at  = models.DateTimeField("Date sent", auto_now_add=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.email}"

