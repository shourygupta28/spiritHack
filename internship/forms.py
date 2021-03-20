from django import forms
from .models import *


class ProjectInternshipForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'field_of_internship',
            'duration',
            'about',
            'location',
            'stipend',
            'skills_required',
            'no_of_internships',
            'perks',
            'who_should_apply',
            'apply_by',
        ]

class InternshipForm(forms.ModelForm):
    class Meta:
        model = StudentInternship
        fields = [
            'startup',
            'duration',
            'stipend',
            'apply_by',
            'link'
        ]

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        fields = [
            'message',
            'resume',
        ]

