from django import forms
from .models import *

class ResourceForm(forms.ModelForm):
	
	class Meta(forms.ModelForm):
		model 		= Resource
		fields 		= ['Subject', 'title','description','file']
