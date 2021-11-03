from django.shortcuts import render
from django.urls.base import response, reverse

from .models import Person
from .forms import PersonForm

# Create your views here.

def home(request):
	return render(request, 'leave/home.html')
