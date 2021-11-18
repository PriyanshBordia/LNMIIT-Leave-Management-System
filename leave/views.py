from django.shortcuts import render

from .models import Person
from .forms import PersonForm

# Create your views here.

def home(request):
	return render(request, 'leave/home.html', context={})

def details(request):
	return render(request, 'leave/details.html', context={})
