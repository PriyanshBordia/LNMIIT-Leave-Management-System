from django import forms
from django.contrib.auth.models import User

from .models import Application, Person


class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = '__all__'
		# ['first_name', 'last_name', 'email', 'username', 'password']

class PersonForm(forms.ModelForm):

	class Meta:
		model = Person
		fields = '__all__'


class ApplicationForm(forms.ModelForm):

	class Meta:
		model = Application
		fields = '__all__'
