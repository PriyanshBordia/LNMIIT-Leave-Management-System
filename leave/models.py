from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import SlugField

# Create your models here.


class Person(models.Model):

	PERSON_ROLES = (
		('DR', 'Director'),
		('DN', 'Dean'),
		('HOD', 'Head of Department'),
		('F', 'Faculty'),
		('VF', 'Visiting Faculty'),
		('S', 'Staff'),
	)

	user = models.OneToOneField(User)
	
	e_id = models.CharField(max_length=10, unique=True)

	role = models.CharField(max_length=5, choices=PERSON_ROLES)
	designation = models.CharField(max_length=255)

	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	slug = models.SlugField(unique=True)

	def __str__(self):
		return f'{self.e_id}. {self.first_name} {self.last_name}'