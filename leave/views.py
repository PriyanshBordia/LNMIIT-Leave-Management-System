from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.decorators.http import require_http_methods

from utils.utility import send_application_mail

from .forms import ApplicationForm, PersonForm, UserForm
from .models import Application, Person

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
					application = Application.objects.filter(person=person).order_by('-created_at').first()
				if person.role == Person.STAFF:
					up_next = Person.objects.filter(department=person.department, role=Person.HEAD_OF_DEPARTMENT).first()
				else:
					up_next = Person.objects.filter(department=person.department, role=Person.HEAD_OF_STAFF).first()
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
		applications = Application.objects.filter(up_next_id=request.user.person.id, status=Application.PENDING).order_by('-created_at')
		return render(request, 'leave/status.html', context={'applications': applications})
	except Application.DoesNotExist:
		return render(request, 'leave/error.html', context={})


@login_required
@require_http_methods(["GET", "POST"])
def approve(request, application_id):
	try:
		application = Application.objects.get(pk=application_id)
		try:
			if application.up_next.role == Person.HEAD_OF_STAFF:
				if Person.objects.filter(role=Person.REGISTRAR).exists():
					up_next = Person.objects.filter(role=Person.REGISTRAR).first()
				else:
					application.status = Application.REJECTED
					up_next = request.user.person
			elif application.up_next.role == Person.REGISTRAR:
				application.status = Application.APPROVED
				person = Person.objects.get(pk=application.person.id)
				up_next = person
				if person.leave_count > 0:
					person.leave_count -= 1
					person.save()
				else:
					return render(request, 'leave/error.html', context={'message': 'You have no leaves left.'})
			elif application.up_next.role == Person.DEAN_OF_FACULTY_AFFAIRS:
				if Person.objects.filter(role=Person.DIRECTOR).exists():
					up_next = Person.objects.filter(role=Person.DIRECTOR).first()
				else:
					application.status = Application.REJECTED
					up_next = request.user.person
			elif application.up_next.role == Person.DIRECTOR:
				application.status = Application.APPROVED
				person = Person.objects.get(pk=application.person.id)
				up_next = person
				if person.leave_count > 0:
					person.leave_count -= 1
					person.save()
				else:
					return render(request, 'leave/error.html', context={'message': 'You have no leaves left.'})
			else:
				return render(request, 'leave/error.html', context={})
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
