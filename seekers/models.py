from django.db import models
from django.conf import settings

class DonationRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests')
    title = models.CharField(max_length=200)
    patient_name = models.CharField(max_length=100)
    description = models.TextField()
    hospital_name = models.CharField(max_length=200)
    diagnosis = models.CharField(max_length=200)
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_raised = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_granted = models.BooleanField(default=False) # Whether admin has given money to seeker
    is_submitted = models.BooleanField(default=False)  # Seeker has submitted for admin review
    is_cancelled = models.BooleanField(default=False)  # Seeker cancelled the campaign
    is_rejected = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)

    account_holder_name = models.CharField(max_length=200, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.patient_name}"

    def progress_percentage(self):
        if self.goal_amount == 0:
            return 0
        return int((self.amount_raised / self.goal_amount) * 100)

class MedicalDocument(models.Model):
    DOC_TYPES = (
        ('CERT', 'Medical Certificate'),
        ('ID', 'Government ID / Identity Proof'),
        ('BANK', 'Bank Passbook'),
        ('PHOTO', 'Patient Photo'),
        ('OTHER', 'Other Document'),
    )
    request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='medical_documents/')
    document_type = models.CharField(max_length=10, choices=DOC_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.request.title}"
