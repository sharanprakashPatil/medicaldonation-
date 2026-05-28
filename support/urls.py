from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_ticket, name='create_ticket'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('ticket/<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('admin/tickets/', views.admin_ticket_list, name='admin_ticket_list'),
    path('admin/ticket/<str:ticket_id>/', views.admin_ticket_detail, name='admin_ticket_detail'),
]
