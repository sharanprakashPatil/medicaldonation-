from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_request, name='create_request'),
    path('upload/<int:pk>/', views.upload_documents, name='upload_documents'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('submit/<int:pk>/', views.submit_for_review, name='submit_for_review'),
    path('cancel/<int:pk>/', views.cancel_campaign, name='cancel_campaign'),
    path('edit/<int:pk>/', views.edit_request, name='edit_request'),
]
