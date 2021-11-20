from django import forms

from .models import Application, Person

class PersonForm(forms.ModelForm):
	
	class Meta:
		model = Person
		fields = '__all__'


class ApplicationForm(forms.ModelForm):

	class Meta:
		model = Application
		fields = '__all__'
