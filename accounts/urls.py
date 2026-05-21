from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_choice, name='register'),
    path('register/seeker/', views.seeker_register, name='seeker_register'),
    path('register/donor/', views.donor_register, name='donor_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
