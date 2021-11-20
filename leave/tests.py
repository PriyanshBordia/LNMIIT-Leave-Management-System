from django.test import TestCase
from django.urls import reverse, resolve
from django.core.management import call_command

from .models import Person, Application
from . import views

# Create your tests here.

class UrlsTestCase(TestCase):

	def test_url_home(self):
		url = reverse('home')
		self.assertEquals(resolve(url).func, views.home)
	
	def test_url_details(self):
		url = reverse('details')
		self.assertEquals(resolve(url).func, views.details)
	
	def test_url_application(self):
		url = reverse('application')
		self.assertEquals(resolve(url).func, views.application)
	
	def test_url_details(self):
		url = reverse('details')
		self.assertEquals(resolve(url).func, views.details)
	
	def test_url_users(self):
		url = reverse('users')
		self.assertEquals(resolve(url).func, views.users)

	def test_url_error(self):
		url = reverse('error')
		self.assertEquals(resolve(url).func, views.error)

class ViewsTestCase(TestCase):

	def test_view_status_code_home(self):
		response = self.client.get(reverse('home'))
		self.assertEquals(response.status_code, 200)

	def test_view_template_used_home(self):
		response = self.client.get(reverse('home'))
		self.assertTemplateUsed(response, 'leave/home.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')
	
	def test_view_status_code_home(self):
		response = self.client.get(reverse('home'))
		self.assertEquals(response.status_code, 200)

	def test_view_template_used_person(self):
		response = self.client.get(reverse('person'))
		self.assertTemplateUsed(response, 'leave/person.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')

	def test_view_status_code_application(self):
		response = self.client.get(reverse('application'))
		self.assertEquals(response.status_code, 200)

	def test_view_template_used_application(self):
		response = self.client.get(reverse('application'))
		self.assertTemplateUsed(response, 'leave/application.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')

	def test_view_status_code_details(self):
		response = self.client.get(reverse('details'))
		self.assertEquals(response.status_code, 200)	

	def test_view_template_used_details(self):
		response = self.client.get(reverse('details'))
		self.assertTemplateUsed(response, 'leave/details.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')

	def test_view_status_code_users(self):
		self.response = self.client.get(reverse('users'))
		self.assertEquals(self.response.status_code, 200)

	def test_view_template_used_users(self):
		self.response = self.client.get(reverse('users'))
		self.assertTemplateUsed(self.response, "leave/users.html")

	def test_view_status_code_error(self):
		self.response = self.client.get(reverse('error'))
		self.assertEquals(self.response.status_code, 200)

	def test_view_template_used_error(self):
		self.response = self.client.get(reverse('error'))
		self.assertTemplateUsed(self.response, "leave/error.html")


# Test for the templates

class TemplatesTestCase(TestCase):
    def test_validate_templates(self):
        call_command("validate_templates")
