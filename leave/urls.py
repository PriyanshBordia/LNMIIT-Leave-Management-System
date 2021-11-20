from django.urls import path

from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('application/', views.application, name='application'),
	path('status/', views.status, name='status'),
	path('details/', views.details, name='details'),
	path('users/', views.users, name='users'),
	path('error/', views.error, name='error'),
]
