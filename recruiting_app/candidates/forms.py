from django import forms
from .models import CandidateProfile, Application

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['bio', 'skills']  # Update with actual field names

        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'skills': forms.TextInput(attrs={'placeholder': 'Enter something...'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']  # Fields for the job application

        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Write your cover letter here...'}),
            'resume': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),  # Restrict to PDF uploads
        }
