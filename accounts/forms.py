from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SeekerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seeker = True
        if commit:
            user.save()
        return user

class DonorRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_donor = True
        if commit:
            user.save()
        return user
