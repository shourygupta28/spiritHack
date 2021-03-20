from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django.db import transaction
from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegistrationFormTeacher(UserCreationForm):
	# name 				= forms.CharField(max_length=60)
	name 				= forms.CharField(max_length=50)
	email 				= forms.EmailField()

	class Meta(UserCreationForm.Meta):
		model 		= User
		fields 		= ['name','email','password1','password2']

class UserRegistrationFormStudent(UserCreationForm):
	# name 				= forms.CharField(max_length=60)
	name 				= forms.CharField(max_length=50)
	email 				= forms.EmailField()

	class Meta(UserCreationForm.Meta):
		model 		= User
		fields 		= ['name','email','password1','password2']

class UserRegistrationFormCompany(UserCreationForm):
	# name 				= forms.CharField(max_length=60)
	name 				= forms.CharField(max_length=50)
	contact_no 			= PhoneNumberField(help_text='Add country code before the contact no.')
	email 				= forms.EmailField()

	class Meta(UserCreationForm.Meta):
		model 		= User
		fields 		= ['name','email','password1','password2']