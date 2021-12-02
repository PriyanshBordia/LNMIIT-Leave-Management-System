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
@require_http_methods(["GET"])
def person(request):
	try:
		person = Person.objects.get(user_id=request.user.id)
		applications = Application.objects.filter(person=person)
		return render(request, 'leave/person.html', context={'person': person, 'applications': applications})
	except Person.DoesNotExist:
		return render(request, 'leave/error.html', context={})


@login_required
@require_http_methods(["GET", "POST"])
def newApplication(request):
	application = ApplicationForm()
	if request.method == 'POST':
		application = ApplicationForm(request.POST)
		if application.is_valid():
			try:
				application.save()
				person = Person.objects.get(pk=request.user.person.id)
				if Application.objects.filter(person=person).exists():
					application = Application.objects.filter(person=person)[0]
				up_next = Person.objects.filter(department=person.department, role=Person.HEAD_OF_DEPARTMENT)[0]
				application.person = person
				application.up_next = up_next
				application.save()
				send_application_mail(application)
				return HttpResponseRedirect(reverse('person', args=()))
			except Person.DoesNotExist:
				return render(request, 'leave/error.html', context={})
		else:
			return render(request, 'leave/newApplication.html', context={'form': application})
	return render(request, 'leave/newApplication.html', context={'form': application})


@login_required
@require_http_methods(["GET"])
def application(request, application_id):
	try:
		application = Application.objects.get(pk=application_id)
		return render(request, 'leave/application.html', context={'application': application})
	except Application.DoesNotExist:
		return render(request, 'leave/error.html', context={})


@login_required
@require_http_methods(["GET", "POST"])
def status(request):
	try:
		applications = Application.objects.filter(up_next_id=request.user.person.id, status='P').order_by('-created_at')
		return render(request, 'leave/status.html', context={'applications': applications})
	except Application.DoesNotExist:
		return render(request, 'leave/error.html', context={})


@login_required
@require_http_methods(["GET", "POST"])
def approve(request, application_id):
	try:
		application = Application.objects.get(pk=application_id)
		try:
			if application.up_next.role == Person.DEAN_OF_FACULTY_AFFAIRS:
				if Person.objects.filter(role=Person.DIRECTOR).exists():
					up_next = Person.objects.filter(role=Person.DIRECTOR)[0]
				else:
					up_next = request.user.person
			elif application.up_next.role == Person.DIRECTOR:
				application.status = Application.APPROVED
				up_next = Person.objects.get(pk=application.person.id)
			else:
				if Person.objects.filter(role=Person.DEAN_OF_FACULTY_AFFAIRS).exists():
					up_next = Person.objects.filter(role=Person.DEAN_OF_FACULTY_AFFAIRS)[0]
				else:
					up_next = request.user.person
			application.up_next = up_next
			application.save()
			send_application_mail(application)
			return HttpResponseRedirect(reverse('status', args=()))
		except Person.DoesNotExist:
			return render(request, 'leave/error.html', context={})
	except Application.DoesNotExist:
		return render(request, 'leave/error.html', context={})


@login_required
def reject(request, application_id):
	try:
		application = Application.objects.get(pk=application_id)
		application.status = Application.REJECTED
		application.save()
		send_application_mail(application)
		return HttpResponseRedirect(reverse('status', args=()))
	except Application.DoesNotExist:
		return render(request, 'leave/error.html', context={})


@login_required
def update(request):
	form = UserForm()
	if request.POST:
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('user', args=(request.user.id, )))
		else:
			return render(request, 'leave/user.html', context={'form': form})
	return HttpResponseRedirect(reverse('user', args=(request.user.id, )))


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
