from django.contrib import admin
from .models import PaymentTransaction

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'request', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'payment_id', 'request__title')
    readonly_fields = ('order_id', 'payment_id', 'signature', 'created_at')
