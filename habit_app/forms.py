from django import forms
from django.forms import Textarea
from .models import UserProfile

class EditUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'habits']
        widgets = {
            'habits': Textarea(attrs={'cols': 40, 'rows': 5}),
        }