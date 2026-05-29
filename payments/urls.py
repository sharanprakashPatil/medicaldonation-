from django.urls import path
from . import views

urlpatterns = [
    path('initiate/<int:pk>/', views.initiate_payment, name='initiate_payment'),
    path('callback/', views.payment_callback, name='payment_callback'),
    path('transfer/<int:pk>/', views.transfer_funds, name='transfer_funds'),
    path('payout-receipt/<int:pk>/', views.payout_receipt, name='payout_receipt'),
    path('seeker-payout-receipt/<int:pk>/', views.seeker_payout_receipt, name='seeker_payout_receipt'),
]
