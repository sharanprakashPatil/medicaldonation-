from django.db import models
from seekers.models import DonationRequest

class PaymentTransaction(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )
    request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    signature = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.order_id} - {self.status}"

class CampaignPayout(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )
    request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    fund_account_id = models.CharField(max_length=100, blank=True, null=True)
    payout_id = models.CharField(max_length=100, blank=True, null=True)
    payout_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    utr = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payout {self.payout_id} - {self.payout_status}"
