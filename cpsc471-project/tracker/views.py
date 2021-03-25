from django.shortcuts import render # Required for the views page to make use of the render() method
from .models import * # Import all models from the tracker app to use in the views

# Create your views here.
from django.http import HttpResponse

# Main page to pick which user type you are, also display information about the website
def index(request):
    return HttpResponse("This is the tracker index.")

# Login screen for nurses
def nurse_login(request):
    return HttpResponse("This is the login site for the nurse.")

# Login screen for civilian
def civilian_login(request):
    return HttpResponse("This is the login site for the civilian.")

# Civilian Views:
def civilian_homepage(request, hcc_no):
    
    return HttpResponse("This is your information %s")

# Nurse Views:
