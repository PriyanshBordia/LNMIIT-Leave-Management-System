from django.test import TestCase
from django.urls import reverse, resolve
from django.core.management import call_command

from termcolor import cprint

from django.contrib.auth.models import User

from .models import Person, Application
from . import views

# Create your tests here.

class UrlsTestCase(TestCase):

	def test_url_home(self):
		url = reverse('home')
		self.assertEquals(resolve(url).func, views.home)
	
	def test_url_newPerson(self):
		url = reverse('newPerson')
		self.assertEquals(resolve(url).func, views.newPerson)

	def test_url_person(self):
		url = reverse('person')
		self.assertEquals(resolve(url).func, views.person)
	
	def test_url_newApplication(self):
		url = reverse('newApplication')
		self.assertEquals(resolve(url).func, views.newApplication)

	def test_url_application(self):
		url = reverse('application', args=[1])
		self.assertEquals(resolve(url).func, views.application)
	
	def test_url_status(self):
		url = reverse('status')
		self.assertEquals(resolve(url).func, views.status)

	def test_url_approve(self):
		url = reverse('approve', args=[1])
		self.assertEquals(resolve(url).func, views.approve)
	
	def test_url_reject(self):
		url = reverse('reject', args=[1])
		self.assertEquals(resolve(url).func, views.reject)

	def test_url_update(self):
		url = reverse('update')
		self.assertEquals(resolve(url).func, views.update)
	
	def test_url_user(self):
		url = reverse('user', args=[1])
		self.assertEquals(resolve(url).func, views.user)

	def test_url_users(self):
		url = reverse('users')
		self.assertEquals(resolve(url).func, views.users)

	def test_url_error(self):
		url = reverse('error')
		self.assertEquals(resolve(url).func, views.error)


class ViewsTestCase(TestCase):

	def setUp(self):
		h_u = User.objects.create_user(username='test_h', password='test_h')
		u = User.objects.create_user(username='test', password='test')
		hod = Person.objects.create(user=h_u, faculty_id='0', department=Person.COMPUTER_SCIENCE_AND_ENGINEERING, first_name='test', email='test_h@lnmiit.ac.in', role=Person.DEAN_OF_FACULTY_AFFAIRS)
		p = Person.objects.create(user=u, faculty_id='1', department=Person.COMPUTER_SCIENCE_AND_ENGINEERING, first_name='test', email='test@lnmiit.ac.in', role=Person.FACULTY)
		Application.objects.create(person=p, status=Application.PENDING, start_date='2021-11-15', end_date='2021-11-21', hasClasses=True, rescheduled_date='2021-11-21', up_next=hod)
		self.client.post('/account/login/', {'username': 'test', 'password': 'test'})

	def test_view_status_code_home(self):
		response = self.client.get(reverse('home'))
		self.assertEquals(response.status_code, 200)

	def test_view_template_used_home(self):
		response = self.client.get(reverse('home'))
		self.assertTemplateUsed(response, 'leave/home.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')
	
	def test_view_status_code_newPerson(self):
		response = self.client.get(reverse('newPerson'))
		self.assertEquals(response.status_code, 200)

	def test_view_template_used_newPerson(self):
		response = self.client.get(reverse('newPerson'))
		self.assertTemplateUsed(response, 'leave/newPerson.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')

	def test_view_status_code_person(self):
		response = self.client.get(reverse('person'))
		self.assertEquals(response.status_code, 200)

	def test_view_template_used_person(self):
		response = self.client.get(reverse('person'))
		self.assertTemplateUsed(response, 'leave/person.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')

	def test_view_status_code_newApplication(self):
		response = self.client.get(reverse('newApplication'))
		self.assertEquals(response.status_code, 200)

	def test_view_template_used_newApplication(self):
		response = self.client.get(reverse('newApplication'))
		self.assertTemplateUsed(response, 'leave/newApplication.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')

	def test_view_status_code_application(self):
		response = self.client.get(reverse('application', args=[1]))
		self.assertEquals(response.status_code, 200)

	def test_view_template_used_application(self):
		response = self.client.get(reverse('application', args=[1]))
		self.assertTemplateUsed(response, 'leave/application.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')

	def test_view_status_code_status(self):
		response = self.client.get(reverse('status'))
		self.assertEquals(response.status_code, 200)	

	def test_view_template_used_status(self):
		response = self.client.get(reverse('status'))
		self.assertTemplateUsed(response, 'leave/status.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')

	def test_view_status_code_approve(self):
		response = self.client.get(reverse('approve', args=[1]))
		self.assertEquals(response.status_code, 302)	

	def test_view_template_used_approve(self):
		response = self.client.get(reverse('approve', args=[1]))
		response = self.client.get(response.url)
		self.assertTemplateUsed(response, 'leave/status.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')

	def test_view_status_code_reject(self):
		response = self.client.get(reverse('reject', args=[1]))
		self.assertEquals(response.status_code, 302)	

	def test_view_template_used_reject(self):
		response = self.client.get(reverse('reject', args=[1]))
		response = self.client.get(response.url)
		self.assertTemplateUsed(response, 'leave/status.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')

	def test_view_status_code_user(self):
		response = self.client.get(reverse('user', args=[1]))
		self.assertEquals(response.status_code, 200)

	def test_view_template_used_user(self):
		response = self.client.get(reverse('user', args=[1]))
		self.assertTemplateUsed(response, 'leave/user.html')

	def test_view_status_code_users(self):
		self.response = self.client.get(reverse('users'))
		self.assertEquals(self.response.status_code, 200)

	def test_view_template_used_users(self):
		self.response = self.client.get(reverse('users'))
		self.assertTemplateUsed(self.response, 'leave/users.html')

	def test_view_status_code_error(self):
		self.response = self.client.get(reverse('error'))
		self.assertEquals(self.response.status_code, 200)

	def test_view_template_used_error(self):
		self.response = self.client.get(reverse('error'))
		self.assertTemplateUsed(self.response, 'leave/error.html')


# Test for the templates

class TemplatesTestCase(TestCase):
	def test_validate_templates(self):
		call_command("validate_templates")
