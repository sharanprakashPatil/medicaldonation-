from django.db import models
from django.conf import settings
import uuid

class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    )
    CATEGORY_CHOICES = (
        ('VERIFICATION', 'Verification & Documents'),
        ('PAYMENT', 'Payment / Donation Issue'),
        ('ACCOUNT', 'Account & Login Issue'),
        ('CAMPAIGN', 'Campaign Management'),
        ('TECHNICAL', 'Technical Support'),
        ('OTHER', 'Other'),
    )

    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    message = models.TextField()
    admin_reply = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_id} - {self.get_category_display()}"
