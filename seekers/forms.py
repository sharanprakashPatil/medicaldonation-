from django import forms
from .models import DonationRequest, MedicalDocument

class DonationRequestForm(forms.ModelForm):
    class Meta:
        model = DonationRequest
        fields = ['title', 'patient_name', 'description', 'hospital_name', 'diagnosis', 'goal_amount']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class MedicalDocumentForm(forms.ModelForm):
    class Meta:
        model = MedicalDocument
        fields = ['document', 'document_type']
