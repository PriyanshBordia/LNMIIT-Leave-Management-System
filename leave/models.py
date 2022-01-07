from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db.models.fields import SlugField

from django.contrib.auth.models import User

# Create your models here.

class Person(models.Model):
	DIRECTOR = 'DR'
	DEAN_OF_ACADEMIC_AFFAIRS = 'DOAA'
	DEAN_OF_FACULTY_AFFAIRS = 'DOFA'
	DEAN_OF_STUDENT_AFFAIRS = 'DOSA'
	HEAD_OF_DEPARTMENT = 'HOD'
	FACULTY = 'F'
	VISITING_FACULTY = 'VF'
	Registrar = 'RG'
	HEAD_OF_STAFF = 'HOS'
	STAFF = 'S'

	COMPUTER_SCIENCE_AND_ENGINEERING = 'CSE' 
	ELECTRONICS_AND_COMMUNICATION_ENGINEERING = 'ECE'
	MECHANICAL_AND_MECHATRONICS_ENGINEERING = 'ME'
	HUMANITIES_AND_SOCIAL_SCIENCES = 'HSS' 
	MATHEMATICS = 'MH'
	PHYSICS = 'PH'
	NON_TEACHING_STAFF = 'NTS'

	PERSON_ROLES = (
		('DR', 'Director'),
		('DOAA', 'Dean of Academic Affairs'),
		('DOFA', 'Dean of Faculty Affairs'),
		('DOSA', 'Dean of Student Affairs'),
		('HOD', 'Head of Department'),
		('F', 'Faculty'),
		('VF', 'Visiting Faculty'),
		('RG', 'Registrar'),
		('HOS', 'Head of Staff'),
		('S', 'Staff'),
	)

	DEPARTMENT = (
		('CSE', 'Computer Science and Engineering'),
		('ECE', 'Electronics and Communication Engineering'),
		('ME', 'Mechanical and Mechatronics Engineering'),
		('HSS', 'Humanities and Social Sciences'),
		('MH', 'Mathematics'),
		('PH', 'Physics'),
		('NTS', 'Non Teaching Staff'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')

	faculty_id = models.CharField(max_length=10, unique=True)
	leave_count = models.IntegerField(validators=[MinValueValidator(0)], default=22, blank=False, null=False)
	department = models.CharField(max_length=3, choices=DEPARTMENT, blank=False, null=False, default='CSE')

	first_name = models.CharField(max_length=50, validators=[MinLengthValidator(1)], blank=False, null=False)
	last_name = models.CharField(max_length=50, blank=True, null=False)

	email = models.EmailField(blank=False, null=False, unique=True)
	office_no = models.IntegerField(blank=False, null=False, default='0000')

	role = models.CharField(max_length=5, choices=PERSON_ROLES, default='F')

	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	# slug = models.SlugField(unique=True)

	class Meta:
		ordering = ['id']
		verbose_name = 'Person'
		verbose_name_plural = 'Persons'

	def is_director(self):
		return self.role == 'DR'

	def is_dean(self):
		return self.role == 'DN'

	def is_hod(self):
		return self.role == 'HOD'

	def is_valid(self):
		if self.email.split('@')[1] != 'lnmiit.ac.in':
			return False
		return len(self.first_name) > 0 and self.user is not None and self.leave_count >= 0

	def __str__(self):
		return f'{self.id}. {self.first_name} {self.last_name}'


class Application(models.Model):

	PENDING = 'P'
	APPROVED = 'A'
	REJECTED = 'R'

	APPLICATION_STATUS = (
		('P', 'Pending'),
		('A', 'Approved'),
		('R', 'Rejected'),
	)

	person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='applicant', default=1)
	status = models.CharField(max_length=1, choices=APPLICATION_STATUS, default='P')

	start_date = models.DateField(blank=False, null=False)
	end_date = models.DateField(blank=False, null=False)

	hasClasses = models.BooleanField(blank=False, null=False, default=False)
	rescheduled_date = models.DateField(blank=True, null=True)

	up_next = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='up_next', default=1)
	comments = models.TextField(blank=True, null=False)

	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	# slug = models.SlugField(unique=True)

	class Meta:
		ordering = ['start_date', 'end_date']

	def is_valid(self):
		return self.person.is_valid() and self.start_date < self.end_date
		
	def __str__(self):
		return f'{self.id}. {self.person.first_name} {self.person.last_name} - {self.get_status_display()}'


