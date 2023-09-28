from django import forms
from .models import UserProfile

class EditUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']