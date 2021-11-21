from django import forms
from django.contrib.auth.models import User

from .models import Application, Person


class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = '__all__'
		# ['first_name', 'last_name', 'email', 'username', 'password']

class ApplicationForm(forms.ModelForm):

	start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
	end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

	rescheduled_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

	class Meta:
		model = Application
		fields = ['start_date', 'end_date', 'hasClasses', 'rescheduled_date', 'comments']

class PersonForm(forms.ModelForm):

	class Meta:
		model = Person
		fields = '__all__'
