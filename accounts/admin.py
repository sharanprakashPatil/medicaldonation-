from django.contrib import admin
from .models import User, Profile, PasswordResetOTP

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_seeker', 'is_donor', 'is_staff', 'is_active']
    list_filter = ['is_seeker', 'is_donor', 'is_staff', 'is_active']
    search_fields = ['username', 'email']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'state']
    search_fields = ['user__username']

@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'is_used']
    list_filter = ['is_used']
