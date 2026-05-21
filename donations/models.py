from django.db import models
from django.conf import settings
from seekers.models import DonationRequest

class Donation(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, related_name='public_donations')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    donor_name = models.CharField(max_length=100, default="Anonymous")
    donor_email = models.EmailField()
    payment_id = models.CharField(max_length=100) # Razorpay payment ID
    order_id = models.CharField(max_length=100)   # Razorpay order ID
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation of {self.amount} for {self.request.title}"
