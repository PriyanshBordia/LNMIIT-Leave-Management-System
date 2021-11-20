from django.shortcuts import render

from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Person, Application
from .forms import PersonForm, ApplicationForm

# Create your views here.

def home(request):
	return render(request, 'leave/home.html', context={})


@login_required
@require_http_methods(["GET", "POST"])
def person(request):
	person = PersonForm()
	if request.method == 'POST':
		person = PersonForm(request.POST)
		if person.is_valid():
			person.save()
			return render(request, 'leave/person.html', context={'form': person})
		else:
			return render(request, 'leave/person.html', context={'form': person})
	return render(request, 'leave/person.html', context={'form': person})


@require_http_methods(["GET", "POST"])
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


@require_http_methods(["GET", "POST"])
def status(request):
	return render(request, 'leave/status.html', context={})

# def applications(request):
# 	pending_applications = Application.objects.all(state=Application.PENDING)


@require_http_methods(["GET", "POST"])
def details(request):
	return render(request, 'leave/details.html', context={})

@login_required
def users(request):
	users = User.objects.all()
	return render(request, 'leave/users.html', context={'users': users})

@login_required
def error(request):
	return render(request, 'leave/error.html', context={"message": "Incompatible DataType.!!", "type": "Type Error", "link": "home"})
