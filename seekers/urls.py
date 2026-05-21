from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_request, name='create_request'),
    path('upload/<int:pk>/', views.upload_documents, name='upload_documents'),
    path('my-requests/', views.my_requests, name='my_requests'),
]
