import datetime
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

	start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
	end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

	rescheduled_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

	def clean(self):
		super(ApplicationForm, self).clean()

		start_date = self.cleaned_data.get('start_date')
		end_date = self.cleaned_data.get('end_date')
		rescheduled_date = self.cleaned_data.get('rescheduled_date')

		# if start_date < datetime.date or end_date < datetime.date or rescheduled_date < datetime.date.now() or start_date > end_date or rescheduled_date >= start_date or rescheduled_date <= end_date:
			# raise forms.ValidationError('Invalid Date')
		return self.cleaned_data
	
	def save(self, commit=True):
		return super(ApplicationForm, self).save(commit=commit)

	class Meta:
		model = Application
		fields = ['start_date', 'end_date', 'hasClasses', 'rescheduled_date', 'comments']
