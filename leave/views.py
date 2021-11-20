from django.shortcuts import render

from django.contrib.auth.models import User

from .models import Person, Application
from .forms import PersonForm, ApplicationForm

# Create your views here.

def home(request):
	return render(request, 'leave/home.html', context={})


def application(request):
	application = ApplicationForm()
	if request.method == 'POST':
		application = ApplicationForm(request.POST)
		if application.is_valid():
			application.save()
			return render(request, 'leave/application.html', context={'form': application})
		else:
			return render(request, 'leave/application.html', context={'form': application})

	return render(request, 'leave/application.html', context={'form': application})


def status(request):
	return render(request, 'leave/status.html', context={})


def details(request):
	return render(request, 'leave/details.html', context={})


def users(request):
	users = User.objects.all()
	return render(request, 'leave/users.html', context={'users': users})

def error(request):
	return render(request, 'leave/error.html', context={})