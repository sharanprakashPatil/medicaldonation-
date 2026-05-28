from django.urls import path
from . import views

urlpatterns = [
    path('', views.donation_list, name='donation_list'),
    path('<int:pk>/', views.donation_detail, name='donation_detail'),
    path('my-donations/', views.my_donations, name='my_donations'),
    path('receipt/<int:pk>/', views.donation_receipt, name='donation_receipt'),
]
