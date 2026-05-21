from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('verify/<int:pk>/', views.verify_request, name='verify_request'),
    path('approve/<int:pk>/', views.approve_request, name='approve_request'),
    path('grant/<int:pk>/', views.grant_money, name='grant_money'),
    path('documents/<int:pk>/', views.view_documents, name='admin_view_documents'),
]
