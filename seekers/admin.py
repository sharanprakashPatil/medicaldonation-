from django.contrib import admin
from .models import DonationRequest, MedicalDocument

@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'goal_amount', 'amount_raised', 'is_verified', 'is_approved', 'is_completed', 'is_granted', 'is_rejected', 'created_at']
    list_filter = ['is_verified', 'is_approved', 'is_completed', 'is_granted', 'is_rejected']
    search_fields = ['title', 'patient_name', 'user__username']
    readonly_fields = ['amount_raised']

@admin.register(MedicalDocument)
class MedicalDocumentAdmin(admin.ModelAdmin):
    list_display = ['request', 'document_type', 'uploaded_at']
    list_filter = ['document_type']
