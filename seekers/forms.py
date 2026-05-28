from django import forms
from .models import DonationRequest, MedicalDocument

class DonationRequestForm(forms.ModelForm):
    class Meta:
        model = DonationRequest
        fields = ['title', 'patient_name', 'description', 'hospital_name', 'diagnosis', 'goal_amount',
                  'account_holder_name', 'account_number', 'bank_name', 'ifsc_code', 'upi_id']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'account_holder_name': forms.TextInput(attrs={'placeholder': 'e.g., John Doe'}),
            'account_number': forms.TextInput(attrs={'placeholder': 'e.g., 12345678901'}),
            'bank_name': forms.TextInput(attrs={'placeholder': 'e.g., State Bank of India'}),
            'ifsc_code': forms.TextInput(attrs={'placeholder': 'e.g., SBIN0001234'}),
            'upi_id': forms.TextInput(attrs={'placeholder': 'e.g., name@upi (optional)'}),
        }
        help_texts = {
            'account_number': 'Enter your bank account number for fund transfers',
            'ifsc_code': '11-character IFSC code of your bank branch',
        }

class MedicalDocumentForm(forms.ModelForm):
    class Meta:
        model = MedicalDocument
        fields = ['document', 'document_type']
