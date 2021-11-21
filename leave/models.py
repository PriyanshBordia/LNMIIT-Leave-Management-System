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

	DEPARTMENT = (
		('CSE', 'Computer Science and Engineering'),
		('ECE', 'Electronics and Communication Engineering'),
		('ME', 'Mechanical-Mechatronics Engineering'),
		('HSS', 'Humanities and Social Sciences'),
		('MH', 'Mathematics'),
		('PH', 'Physics'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')

	faculty_id = models.CharField(max_length=10, unique=True)
	leave_count = models.IntegerField(default=22)
	department = models.CharField(max_length=3, choices=DEPARTMENT, default='CSE')

	first_name = models.CharField(max_length=50, blank=False, null=False)
	last_name = models.CharField(max_length=50, blank=True, null=False)

	email = models.EmailField(blank=False, null=False)
	office_no = models.IntegerField(blank=False, null=False, default='00')

	role = models.CharField(max_length=5, choices=PERSON_ROLES, default='F')

	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	# slug = models.SlugField(unique=True)

	def is_director(self):
		return self.role == 'DR'

	def is_dean(self):
		return self.role == 'DN'

	def is_hod(self):
		return self.role == 'HOD'

	def is_valid(self):
		return len(self.first_name) > 0 and self.user is not None and self.leave_count >= 0

	def __str__(self):
		return f'{self.id}. {self.first_name} {self.last_name}'


class Application(models.Model):
	APPLICATION_STATUS = (
		('P', 'Pending'),
		('A', 'Approved'),
		('R', 'Rejected'),
	)

	person = models.ForeignKey(Person, on_delete=models.CASCADE, default=1)
	status = models.CharField(max_length=1, choices=APPLICATION_STATUS, default='P')

	start_date = models.DateField(blank=False, null=False)
	end_date = models.DateField(blank=False, null=False)

	hasClasses = models.BooleanField(blank=False, null=False, default=False)
	rescheduled_date = models.DateTimeField(blank=True, null=True)

	comments = models.TextField(blank=True, null=False)

	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	# slug = models.SlugField(unique=True)

	def is_valid(self):
		return self.person is not None and self.person.is_valid() and self.start_date is not None and self.end_date is not None and self.start_date < self.end_date
		
	def __str__(self):
		return f'{self.id}. {self.person.first_name} {self.person.last_date} {self.status}'


