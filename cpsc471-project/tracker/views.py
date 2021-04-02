from django.http.response import Http404
from django.shortcuts import render # Required for the views page to make use of the render() method
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.base import TemplateView
from django.template import Context, Template

from .models import * # Import all models from the tracker app to use in the views
from .forms import hcc_form
# Create your views here.
from django.http import HttpResponse

from django.contrib.auth import login


# Main page to pick which user type you are, also display information about the website

def index_view(request):
    return render(request, 'tracker/index.html')

# Login screen for nurses
def nurse_login(request):
    return render(request, 'tracker/civilianlogin.html')

# Login screen for civilian
def civilian_login(request):
    if request.method == 'POST':
        form = hcc_form(request.POST)

        if form.is_valid():
            return redirect('785521144/')
    else:
        form = hcc_form()

    return render(request, 'tracker/civilianlogin.html', {'form':form})

# Civilian Views: #########################################################
def civilian_homepage(request, hcc_no):
    try:
        my_civilian = Civilian.objects.get(hcc_no = hcc_no)
    except Civilian.DoesNotExist:
        raise Http404("Civilian does not exist")
    return HttpResponse("This is your information %s" % my_civilian)

# This endpoint will have to handle a GET and POST request
def new_civilian(request):
    if request.method == 'POST':
        if (request.POST.get('hcc_no') and request.POST.get('phone_no') and request.POST.get('sex') and
            request.POST.get('address') and request.POST.get('age') and request.POST.get('first_name') and
            request.POST.get('last_name') and request.POST.get('doctor_hcc')):
                saverecord = Civilian()
                saverecord.hcc_no = request.POST.get('hcc_no')
                saverecord.phone_no = request.POST.get('phone_no') 
                saverecord.sex = request.POST.get('sex')
                saverecord.address = request.POST.get('address')
                saverecord.age = request.POST.get('age')
                saverecord.first_name = request.POST.get('first_name')
                saverecord.first_name = request.POST.get('last_name')
                saverecord.doctor_hcc = request.POST.get('doctor_hcc')
                saverecord.save()
        return render(request, 'index.html') ##placeholder - if succeessful will redirect to home.

    else: 
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