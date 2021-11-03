from django.contrib import admin

from .models import Person

# Register your models here.

class Person(admin.ModelAdmin):
	model = Person

	list_per_page = 10

admin.site.site_header = 'Admin - The LNMIIT'
admin.site.site_title = "Admin - The LNMIIT"
admin.site.index_title = "Administration"

admin.site.register(Person, Person)