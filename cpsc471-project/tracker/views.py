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
    except Civilian.DoesNotExist:
        raise Http404("Civilian does not exist")
    return HttpResponse("This is your information %s" % my_civilian)

# This endpoint will have to handle a GET and POST request
def new_civilian(request):
    return HttpResponse("This endpoint will contain the field you need to fill out to create a new civilian")

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
#def nurse_homepage(request, hcc_no):
#    try:
#        my_nurse = Nurse.objects.get(hcc_no = hcc_no)
#    except Nurse.DoesNotExist:
#        raise Http404("Nurse does not exist")
#    return HttpResponse("This is your information %s" % my_nurse)

def nurse_homepage(request, hcc_no):
    my_nurse = Nurse.objects.get(hcc_no=hcc_no)
    context_dict = {
        "nurse_obj": my_nurse
    }
    return render(request, 'tracker/nurseHomepage.html', context_dict)

def nurse_appointments(request, hcc_no):
    my_nurse_appointments = Appointment.objects.filter(nurse_hcc_no=hcc_no)
    context_dict = {
        "nurse_obj": my_nurse_appointments
    }
    return render(request, 'tracker/nurseAppointments.html', context_dict)

def nurse_vaccines(request):
    my_vaccines = Vaccine.objects.filter()
    context_dict = {
        "vaccine_obj": my_vaccines
    }
    return render(request, 'tracker/nurseVaccines.html', context_dict)

def nurse_vaccine_details(request, DIN_no):
    my_vaccine = Vaccine.objects.get(DIN_no=DIN_no)
    my_vaccine_details = VaccineSideEffect.objects.filter(vaccine_DIN_no=DIN_no)
    my_stored_at = StoredAt.objects.filter(DIN_no=DIN_no)
    my_disposed_at = DisposedAt.objects.filter(DIN_no=DIN_no)
    context_dict = {
        "vaccine_obj": my_vaccine,
        "vaccine_side_effect_obj": my_vaccine_details,
        "stored_at_obj": my_stored_at,
        "disposed_at_obj": my_disposed_at
    }
    return render(request, 'tracker/nurseVaccineDetails.html', context_dict)

def nurse_ppe(request, hcc_no):
    my_nurse_ppe = Ppe.objects.filter(nurse_hcc=hcc_no)
    context_dict = {
        "nurse_obj": my_nurse_ppe
    }
    return render(request, 'tracker/nursePpe.html', context_dict)


# This endpoint will have to handle a GET and POST request
# GET - display the fields that the user needs to fill it
# POST - upon button click, validate the fields and save the new item to the database
def new_nurse(request):
    return HttpResponse("This endpoint will contain the field you need to fill out to create a new nurse")

# This endpoint will have to handle a GET and POST request
# GET - get the current values of the nurse and display in editable fields
# POST - upon button click, validate fields and update if correct
def edit_nurse(request, hcc_no):
    try:
        my_nurse = Nurse.objects.get(hcc_no = hcc_no)
    except Nurse.DoesNotExist:
        raise Http404("Nurse does not exist")
    return HttpResponse("This will let you edit this nurse: %s" % my_nurse)