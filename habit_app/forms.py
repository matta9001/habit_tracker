from django import forms
from .models import UserProfile

class BioForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']