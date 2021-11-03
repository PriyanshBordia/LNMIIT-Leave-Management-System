from django.urls import path

from . import views

url_patterns = [
	path('', views.home, name='home'),
	path('/details', views.details, name='details'),
]