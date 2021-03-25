from django.http.response import Http404
from django.shortcuts import render # Required for the views page to make use of the render() method
from .models import * # Import all models from the tracker app to use in the views

# Create your views here.
from django.http import HttpResponse

# Main page to pick which user type you are, also display information about the website
def index(request):
    return HttpResponse("This is the index page, we will implement the login selection page here. (Choose civilian or nurse and get sent to the login pages)")

# Login screen for nurses
def nurse_login(request):
    return HttpResponse("This is the login site for the nurse. (You will be able to enter your nurse HCC and press login)")

# Login screen for civilian
def civilian_login(request):
    return HttpResponse("This is the login site for the civilian. (You will be able to enter your civilian HCC and press login)")

# Civilian Views: #########################################################
def civilian_homepage(request, hcc_no):
    try:
        my_civilian = Civilian.objects.get(hcc_no = hcc_no)
    except Civilian.DoesNotExist:
        raise Http404("Civilian does not exist")
    return HttpResponse("This is your information %s" % my_civilian)

def new_civilian(request):
    return HttpResponse("This endpoint will contain the field you need to fill out to create a new civilian")

def edit_civilian(request, hcc_no):
    try:
        my_civilian = Civilian.objects.get(hcc_no = hcc_no)
    except Civilian.DoesNotExist:
        raise Http404("Civilian does not exist")
    return HttpResponse("This will let you edit this civilian: %s" % my_civilian)


# Nurse Views: #########################################################
def nurse_homepage(request, hcc_no):
    try:
        my_nurse = Nurse.objects.get(hcc_no = hcc_no)
    except Nurse.DoesNotExist:
        raise Http404("Nurse does not exist")
    return HttpResponse("This is your information %s" % my_nurse)

def new_nurse(request):
    return HttpResponse("This endpoint will contain the field you need to fill out to create a new nurse")

def edit_nurse(request, hcc_no):
    try:
        my_nurse = Nurse.objects.get(hcc_no = hcc_no)
    except Nurse.DoesNotExist:
        raise Http404("Nurse does not exist")
    return HttpResponse("This will let you edit this nurse: %s" % my_nurse)