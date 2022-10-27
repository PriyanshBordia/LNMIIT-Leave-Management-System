from django.contrib import admin

from .models import Application, Person

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
	model = Person
	list_per_page = 10


class ApplicationAdmin(admin.ModelAdmin):
	model = Application
	list_per_page = 10


admin.site.site_header = 'Admin LMS - The LNMIIT'
admin.site.site_title = "LMS - The LNMIIT"
admin.site.index_title = "Admin"

admin.site.register(Person, PersonAdmin)
admin.site.register(Application, ApplicationAdmin)
