from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm,
    PasswordResetForm, SetPasswordForm
)
from django.utils.translation import gettext_lazy as _
from .models import Profile, Order, Review, ContactMessage
import re

User = get_user_model()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    phone = forms.CharField(max_length=20, required=False)
    newsletter = forms.BooleanField(required=False)
    terms = forms.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Обновляем профиль
            user.profile.phone = self.cleaned_data.get('phone', '')
            user.profile.newsletter = self.cleaned_data.get('newsletter', False)
            user.profile.save()
        
        return user

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'city', 'address', 'postal_code']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full border px-4 py-2'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border px-4 py-2'}),
            'city': forms.TextInput(attrs={'class': 'w-full border px-4 py-2'}),
            'address': forms.TextInput(attrs={'class': 'w-full border px-4 py-2'}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full border px-4 py-2'}),
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))
    remember = forms.BooleanField(required=False, initial=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'


class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('No user with this email address was found')
        return email


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True, disabled=True)
    phone = forms.CharField(max_length=20, required=False)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    newsletter = forms.BooleanField(required=False)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['phone'].initial = self.instance.profile.phone
            self.fields['birth_date'].initial = self.instance.profile.birth_date
            self.fields['newsletter'].initial = self.instance.profile.newsletter
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            # Обновляем профиль
            user.profile.phone = self.cleaned_data.get('phone', '')
            user.profile.birth_date = self.cleaned_data.get('birth_date')
            user.profile.newsletter = self.cleaned_data.get('newsletter', False)
            user.profile.save()
        
        return user


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError('Invalid current password')
        return current_password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')
        
        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise forms.ValidationError('The passwords don\'t match')
        
        return cleaned_data
    

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input-field'}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'input-field'}),
        strip=False,
    )
    terms = forms.BooleanField(
        required=True,
        label=_("I agree to the Terms and Privacy Policy"),
    )
    newsletter = forms.BooleanField(
        required=False,
        label=_("I want to receive news and special offers by email"),
    )
    
    class Meta(UserCreationForm.Meta):
        model  = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
            'first_name': forms.TextInput(attrs={'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field'}),
            'phone': forms.TextInput(attrs={'class': 'input-field'}),
        }
        

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'input-field'}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input-field'}),
    )
    remember_me = forms.BooleanField(
        required=False,
        label=_("Remember me")
    )

    class Meta:
        model = User
        fields = ('email', 'password')

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'input-field'}),
    )


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'address', 'city', 'postal_code']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full border rounded p-2',
                'rows': 4,
                'placeholder': 'Write your review...'
            })
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-field', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'input-field', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'input-field', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'input-field'}),
            'message': forms.Textarea(attrs={'class': 'input-field', 'rows': 5}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not forms.EmailField().clean(email):
            raise forms.ValidationError("Enter a valid email.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\+?\d{7,15}$', phone):
            raise forms.ValidationError("Enter the correct phone number (digits only, 7 to 15 characters).")
        return phone
