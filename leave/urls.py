from django.urls import path

from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('newPerson/', views.newPerson, name='newPerson'),
	path('application/', views.application, name='application'),
	path('status/', views.status, name='status'),
	path('details/', views.details, name='details'),
	path('update/', views.update, name='update'),
	path('user/<int:user_id>', views.user, name='user'),
	path('users/', views.users, name='users'),
	path('error/', views.error, name='error'),
]
