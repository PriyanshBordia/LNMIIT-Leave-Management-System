from django.urls import path

from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('newPerson/', views.newPerson, name='newPerson'),
	path('person/', views.person, name='person'),
	path('newApplication/', views.newApplication, name='newApplication'),
	path('application/<int:application_id>', views.application, name='application'),
	path('status/', views.status, name='status'),
	path('approve/<int:application_id>', views.approve, name='approve'),
	path('reject/<int:application_id>', views.reject, name='reject'),
	path('update/', views.update, name='update'),
	path('user/<int:user_id>', views.user, name='user'),
	path('users/', views.users, name='users'),
	path('error/', views.error, name='error'),
]
