from django.contrib import admin
from .models import SupportTicket

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'user', 'category', 'status', 'created_at']
    list_filter = ['status', 'category']
    search_fields = ['ticket_id', 'user__username']
    readonly_fields = ['ticket_id', 'created_at', 'updated_at']
