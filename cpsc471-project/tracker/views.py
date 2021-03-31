from django.http.response import Http404
from django.shortcuts import render # Required for the views page to make use of the render() method
from django.views import generic
from django.views.generic.base import TemplateView
from django.template import Context, Template

from .models import * # Import all models from the tracker app to use in the views

# Create your views here.
from django.http import HttpResponse

# Main page to pick which user type you are, also display information about the website

def index_view(request):
    return render(request, 'tracker/index.html')

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
        my_health_conditions = HealthCondition.objects.filter(hcc_no = hcc_no)
        context = {
            "my_civilian": my_civilian,
            "my_health_conditions": my_health_conditions
        }

        return render(request, "tracker/civilian_homepage.html", context)
    except Civilian.DoesNotExist:
        raise Http404("Civilian does not exist")
    except HealthCondition.DoesNotExist:
        context = {
            "my_civilian": my_civilian,
        }
        
        return render(request, "tracker/civilian_homepage.html", context)

# This endpoint will have to handle a GET and POST request
def new_civilian(request):
    return render(request, "tracker/civilianregistration.html")

# This endpoint will have to handle a GET and POST request
def edit_civilian(request, hcc_no):
    try:
        my_civilian = Civilian.objects.get(hcc_no = hcc_no)
    except Civilian.DoesNotExist:
        raise Http404("Civilian does not exist")
    return HttpResponse("This will let you edit this civilian: %s" % my_civilian)

def civilian_riskfactor(request, hcc_no):
    try:
        my_riskfactor = RiskFactor.objects.get(hcc_no = hcc_no)
    except RiskFactor.DoesNotExist:
        raise Http404("Risk factor does not exist for this civilian")
    return HttpResponse("This will let you view the risk factor: %s" % my_riskfactor)


# Nurse Views: #########################################################
def nurse_homepage(request, hcc_no):
    try:
        my_nurse = Nurse.objects.get(hcc_no = hcc_no)
    except Nurse.DoesNotExist:
        raise Http404("Nurse does not exist")
    return HttpResponse("This is your information %s" % my_nurse)

# This endpoint will have to handle a GET and POST request
# GET - display the fields that the user needs to fill it
# POST - upon button click, validate the fields and save the new item to the database
def new_nurse(request):
    return render(request, "tracker/nurseregistration.html")

# This endpoint will have to handle a GET and POST request
# GET - get the current values of the nurse and display in editable fields
# POST - upon button click, validate fields and update if correct
def edit_nurse(request, hcc_no):
    try:
        my_nurse = Nurse.objects.get(hcc_no = hcc_no)
    except Nurse.DoesNotExist:
        raise Http404("Nurse does not exist")
    return HttpResponse("This will let you edit this nurse: %s" % my_nurse)