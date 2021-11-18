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
		# ('S', 'Staff'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')

	faculty_id = models.CharField(max_length=10, unique=True)

	first_name = models.CharField(max_length=50, blank=False, null=False)
	last_name = models.CharField(max_length=50, blank=True, null=False)

	email = models.EmailField(blank=False, null=False)
	office_no = models.IntegerField(blank=True, null=False)

	role = models.CharField(max_length=5, choices=PERSON_ROLES, default='F')
	designation = models.CharField(max_length=255)

	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	slug = models.SlugField(unique=True)

	def is_director(self):
		return self.role == 'DR'

	def is_dean(self):
		return self.role == 'DN'

	def is_valid(self):
		return len(self.first_name) > 0 and self.user is not None

	def __str__(self):
		return f'{self.id}. {self.first_name} {self.last_name}'


class Application(models.Model):
	APPLICATION_STATUS = (
		('P', 'Pending'),
		('A', 'Approved'),
		('R', 'Rejected'),
	)

	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	status = models.CharField(max_length=1, choices=APPLICATION_STATUS, default='P')

	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	