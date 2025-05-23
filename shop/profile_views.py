from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm


@login_required
def profile_view(request):
    """
    User profile page view
    """
    return render(request, 'shop/profile.html')


@login_required
def edit_profile_view(request):
    """
    Edit user profile view
    """
    user = request.user
    
    if request.method == 'POST':
        # Here you can add logic to update user profile
        # You would need to create a ProfileEditForm for this
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        newsletter = request.POST.get('newsletter') == 'on'
        
        # Update user data
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.newsletter = newsletter
        user.save()
        
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('profile')
    
    return render(request, 'shop/edit_profile.html', {'user': user})


@login_required
def change_password_view(request):
    """
    Change password view
    """
    if request.method == 'POST':
        # Here you would validate the old password and set the new one
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        # Check if old password is correct
        if not request.user.check_password(old_password):
            messages.error(request, "Your old password was entered incorrectly.")
            return redirect('change_password')
        
        # Check if new passwords match
        if new_password1 != new_password2:
            messages.error(request, "The two password fields didn't match.")
            return redirect('change_password')
        
        # Set new password
        request.user.set_password(new_password1)
        request.user.save()
        
        messages.success(request, "Your password was successfully updated!")
        return redirect('profile')
    
    return render(request, 'shop/change_password.html')


# Additional view for social auth success
def social_auth_success(request):
    return redirect('home')