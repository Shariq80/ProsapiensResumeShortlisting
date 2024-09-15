from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'email', 'phone_number', 'resume', 'years_of_experience', 'education']
