from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SeekerRegistrationForm, DonorRegistrationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings
from .models import User, PasswordResetOTP
import random
import string

def register_choice(request):
    return render(request, 'accounts/register_choice.html')

def seeker_register(request):
    if request.method == 'POST':
        form = SeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! You can now create a donation request.")
            return redirect('dashboard')
    else:
        form = SeekerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'type': 'Seeker'})

def donor_register(request):
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to Medical Hope.")
            return redirect('dashboard')
    else:
        form = DonorRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'type': 'Donor'})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login_type = request.POST.get('login_type', 'user')
                if login_type == 'admin':
                    if user.is_staff:
                        login(request, user)
                        return redirect('admin_dashboard')
                    messages.error(request, "This account does not have admin access.")
                    return render(request, 'accounts/login.html', {'form': form})
                role = request.POST.get('role')
                if role == 'donor' and not user.is_donor:
                    messages.error(request, "This account is not registered as a Donor.")
                    return render(request, 'accounts/login.html', {'form': form})
                if role == 'seeker' and not user.is_seeker:
                    messages.error(request, "This account is not registered as a Seeker.")
                    return render(request, 'accounts/login.html', {'form': form})
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp = ''.join(random.choices(string.digits, k=6))
            PasswordResetOTP.objects.create(user=user, otp=otp)
            
            send_mail(
                'Your Password Reset OTP',
                f'Your OTP for password reset is {otp}. It is valid for 10 minutes.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            request.session['reset_email'] = email
            messages.success(request, "OTP has been sent to your email.")
            return redirect('verify_otp')
        else:
            messages.error(request, "User with this email does not exist.")
    return render(request, 'accounts/forgot_password.html')

def verify_otp(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
    
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, "User not found.")
            return redirect('forgot_password')
        otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp_entered).last()
        
        if otp_obj and otp_obj.is_valid():
            otp_obj.is_used = True
            otp_obj.save()
            request.session['otp_verified'] = True
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid or expired OTP.")
            
    return render(request, 'accounts/verify_otp.html')

def reset_password(request):
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')
    
    email = request.session.get('reset_email')
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            user = User.objects.filter(email=email).first()
            if not user:
                messages.error(request, "User not found.")
                return redirect('forgot_password')
            user.set_password(password)
            user.save()
            del request.session['reset_email']
            del request.session['otp_verified']
            messages.success(request, "Password reset successful. You can now login.")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
            
    return render(request, 'accounts/reset_password.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone_number = request.POST.get('phone_number', '')
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    return render(request, 'accounts/profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return redirect('profile')
