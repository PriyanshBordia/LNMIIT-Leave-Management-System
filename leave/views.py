from django.contrib import messages
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
		messages.warning(request, 'Person does not exist.')
		return HttpResponseRedirect("../person")


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
				if person.role in [Person.FACULTY, Person.VISITING_FACULTY]:
					try:
						up_next = Person.objects.get(department=person.department, role=Person.HEAD_OF_DEPARTMENT)
					except Person.DoesNotExist:
						up_next = person				
				else:
					try:
						up_next = Person.objects.get(role=Person.HEAD_OF_STAFF)
					except Person.DoesNotExist:
						up_next = person	
				application.person = person
				application.up_next = up_next
				application.save()
				send_application_mail(application)
				return HttpResponseRedirect(reverse('person', args=()))
			except Person.DoesNotExist:
				messages.error(request, f'Person does not exist.')
				return HttpResponseRedirect("../person")
		else:
			return render(request, 'leave/newApplication.html', context={'form': application})
	return render(request, 'leave/newApplication.html', context={'form': application})


@login_required
@require_http_methods(["GET"])
def application(request, application_id: int):
	try:
		application = Application.objects.get(pk=application_id)
		return render(request, 'leave/application.html', context={'application': application})
	except Application.DoesNotExist:
		messages.error(request, f'Application with id: {application_id} does not exist.')
		return HttpResponseRedirect("../status")


@login_required
@require_http_methods(["GET", "POST"])
def status(request, type: str):
	try:
		if type == "pending":
			applications = Application.objects.filter(up_next_id=request.user.person.id, status=Application.PENDING).order_by('-created_at')
		elif type == "approved":
			applications = Application.objects.filter(person__department=request.user.person.department, status=Application.APPROVED).order_by('-created_at')
		elif type == "rejected":
			applications = Application.objects.filter(person__department=request.user.person.department, status=Application.REJECTED).order_by('-created_at')
		return render(request, 'leave/status.html', context={'applications': applications, 'type': type})
	except Application.DoesNotExist:
		messages.error(request, f'Application does not exist.')
		return HttpResponseRedirect("../person")


@login_required
@require_http_methods(["GET", "POST"])
def approve(request, application_id: int):
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
			elif application.up_next.role == Person.HEAD_OF_DEPARTMENT:
				if Person.objects.filter(role=Person.DEAN_OF_FACULTY_AFFAIRS).exists():
					up_next = Person.objects.filter(role=Person.DEAN_OF_FACULTY_AFFAIRS).first()
				else:
					application.status = Application.REJECTED
					up_next = request.user.person
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
			else:
				messages.error(request, 'Error in approving application.')
				return HttpResponseRedirect("../status")
			application.up_next = up_next
			application.save()
			send_application_mail(application)
			return HttpResponseRedirect(reverse('status', args=()))
		except Person.DoesNotExist:
			messages.error(request, "Person does not exist")
			return HttpResponseRedirect("../status")
	except Application.DoesNotExist:
		messages.error(request, f'Application with id: {application_id} does not exist.')
		return HttpResponseRedirect("../status")

@login_required
def reject(request, application_id: int):
	try:
		application = Application.objects.get(pk=application_id)
		application.status = Application.REJECTED
		application.save()
		send_application_mail(application)
		return HttpResponseRedirect(reverse('status', args=()))
	except Application.DoesNotExist:
		messages.error(request, f'Application with id: {application_id} does not exist.')
		return HttpResponseRedirect("../status")


@login_required
def update(request):
	try:
		form = UserForm()
		if request.POST:
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('user', args=(request.user.id, )))
			else:
				return render(request, 'leave/user.html', context={'form': form})
		return HttpResponseRedirect(reverse('user', args=(request.user.id, )))
	except Exception as e:
		messages.error(request, str(e))
		return HttpResponseRedirect("../home")


@login_required
def user(request, user_id):
	try:
		user = User.objects.get(pk=user_id)
		return render(request, 'leave/user.html', context={"user": user})
	except User.DoesNotExist:
		messages.error(request, "User Doesn't Exist")
		return HttpResponseRedirect("../home")


@login_required
def users(request):
	users = User.objects.all()
	return render(request, 'leave/users.html', context={'users': users})


@login_required
def error(request):
	return render(request, 'leave/error.html', context={"message": "Error test.", "type": "Type Error", "link": "home"})
