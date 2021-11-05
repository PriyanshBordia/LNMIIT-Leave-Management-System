from django.test import TestCase
from django.urls import reverse, resolve

from . import views

# Create your tests here.


class UrlsTestCase(TestCase):

	def test_url_home(self):
		url = reverse('home')
		self.assertEquals(resolve(url).func, views.home)
	
	def test_url_details(self):
		url = reverse('details', args=['1'])
		self.assertEquals(resolve(url).func, views.details)

class ViewsTestCase(TestCase):

	def test_view_status_code_home(self):
		response = self.client.get(reverse('home'))
		self.assertEquals(response.status_code, 200)

	def test_view_template_used_home(self):
		response = self.client.get(reverse('home'))
		self.assertTemplateUsed(response, 'leave/home.html')
		self.assertTemplateNotUsed(response, 'leave/error.html')

	def test_details(self):
		response = self.client.get(reverse('details', args=['1']))
		self.assertEquals(response.status_code, 200)	
