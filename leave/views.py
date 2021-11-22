from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse

from utils.utility import send_application_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods

from .models import Application, Person
from .forms import UserForm, ApplicationForm, PersonForm 

# Create your views here.

def home(request):
	return render(request, 'leave/home.html', context={})


@login_required
@require_http_methods(["GET", "POST"])
def newPerson(request):
	person = PersonForm()
	if request.method == 'POST':
		person = PersonForm(request.POST)
		if person.is_valid():
			person.save()
			return render(request, 'leave/person.html', context={'form': person})
		else:
			return render(request, 'leave/newPerson.html', context={'form': person})
	return render(request, 'leave/newPerson.html', context={'form': person})


@login_required
@require_http_methods(["GET", "POST"])
def person(request):
	try:
		person = Person.objects.get(user_id=request.user.id)
		applications = Application.objects.filter(person=person)
		return render(request, 'leave/person.html', context={'person': person, 'applications': applications})
	except Person.DoesNotExist:
		return render(request, 'leave/error.html', context={})


@require_http_methods(["GET", "POST"])
def application(request):
	application = ApplicationForm()
	if request.method == 'POST':
		application = ApplicationForm(request.POST)
		if application.is_valid():
			send_application_mail(request.user, application)
			application.save()
			return HttpResponseRedirect(reverse('person', args=()))
		else:
			return render(request, 'leave/application.html', context={'form': application})
	return render(request, 'leave/application.html', context={'form': application})


@require_http_methods(["GET", "POST"])
def status(request):
	return render(request, 'leave/status.html', context={})


@login_required
def update(request):
	user_id = request.user.id
	form = UserForm()
	if request.POST:
		if form.is_valid():
			form.save()
			return render(request, 'leave/user.html', context={'user': user})
		else:
			return render(request, 'leave/user.html', context={'user': user})
	return HttpResponseRedirect(reverse('user', args=(user_id, )))


@login_required
def user(request, user_id):
	try:
		user = User.objects.get(pk=user_id)
		return render(request, 'leave/user.html', context={"user": user})
	except User.DoesNotExist:
		return render(request, 'leave/error.html', context={"message": "User Doesn't Exist!!", "type": "Value DoesNotExist!!", "link": "users"})


@login_required
def users(request):
	users = User.objects.all()
	return render(request, 'leave/users.html', context={'users': users})


@login_required
def error(request):
	return render(request, 'leave/error.html', context={"message": "Incompatible DataType.!!", "type": "Type Error", "link": "home"})
