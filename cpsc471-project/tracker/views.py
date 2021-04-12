from django.http.response import Http404
from django.shortcuts import render # Required for the views page to make use of the render() method
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie # Used to silence CORS issues with postman

from .models import * # Import all models from the tracker app to use in the views
from .forms import hcc_form

from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib import messages

import sys
import random

import datetime 
from datetime import timedelta


# Main page to pick which user type you are, also display information about the website

def index_view(request):
    return render(request, 'tracker/index.html')

# Login screen for nurses
@ensure_csrf_cookie
def nurse_login(request):
    error = False
    if request.method == 'POST':
        form = hcc_form(request.POST)
        if form.is_valid():
            hcc_no = int(request.POST.get('nurse-hcc'))
            print('Number in form is: ' + str(hcc_no))
            str_hcc = str(hcc_no)
            length = len(str_hcc)

            if length <= 9:
                #print('yoooo the length of the hcc no is: ' + str(length))
                try:
                    my_nurse = Nurse.objects.get(hcc_no = hcc_no)
                except Nurse.DoesNotExist:
                #if nurse does not exist, then return error screen but let them login
                    error = True
                    messages.error(request, "Specified HealthCare Number does not exist! Please Register or Login with a valid HealthCare Number.")
            else:
                error = True
             #   print('sadge')
                messages.error(request, "Specified HealthCare Number does not exist! Please Register or Login with a valid HealthCare Number.")
            #Now that we got the information, find the corresponding
            
            if error == False:
                return redirect(str(hcc_no)+'/')

    else:
        form = hcc_form()

    return render(request, 'tracker/nurse_login.html')

# Login screen for civilian
@ensure_csrf_cookie
def civilian_login(request):
    error = False
    if request.method == 'POST':
        form = hcc_form(request.POST)

        if form.is_valid():

            hcc_no = int(request.POST.get('civ-hcc'))
            print('Number in form is: ' + str(hcc_no))
            str_hcc = str(hcc_no)
            length = len(str_hcc)

            if length <= 9:
                #print('yoooo the length of the hcc no is: ' + str(length))
                try:
                    my_civilian = Civilian.objects.get(hcc_no = hcc_no)
                except Civilian.DoesNotExist:
                #if civilian does not exist, then return error screen but let them login
                    error = True
                    messages.error(request, "Specified HealthCare Number does not exist! Please Register or Login with a valid HealthCare Number.")
            else:
                error = True
             #   print('sadge')
                messages.error(request, "Specified HealthCare Number does not exist! Please Register or Login with a valid HealthCare Number.")
            #Now that we got the information, find the corresponding
            
            if error == False:
                return redirect(str(hcc_no)+'/')

    else:
        form = hcc_form()

    return render(request, 'tracker/civilian_login.html')

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
        return redirect('/civilian/')

# This endpoint will have to handle a GET and POST request
@ensure_csrf_cookie
def new_civilian(request):
    
    context_dict = {
        "doctor_obj": Doctor.objects.all(),
    }
    error = False
    if request.method == 'POST':
    
        #future to do: check if they exist in db and return to the registration page. 
        if (request.POST.get('hcc_no') and request.POST.get('phone_no') and request.POST.get('sex') and
            request.POST.get('address') and request.POST.get('age') and request.POST.get('first_name') and
            request.POST.get('last_name') and request.POST.get('doctor_hcc')):
                #Check if the civilian already exists, since we don't want to replace existing data
                try:
                    my_civie = Civilian.objects.get(hcc_no = int(request.POST.get('hcc_no')))

                    error = True
                    messages.error(request, "Account already exists! Please Login with your HealthCard Number.")
                except Civilian.DoesNotExist:
                    saverecord = Civilian()
                    saverecord.hcc_no = int(request.POST.get('hcc_no'))
                    saverecord.phone_no = int(request.POST.get('phone_no')) 
                    saverecord.sex = request.POST.get('sex')
                    saverecord.address = request.POST.get('address')
                    saverecord.age = int(request.POST.get('age'))
                    saverecord.first_name = request.POST.get('first_name')
                    saverecord.last_name = request.POST.get('last_name')
                    #attempt to find doctor, return error message to webpage if he doesn't exist
                    saverecord.doctor_hcc = Doctor.objects.get(hcc_no = int (request.POST.get('doctor_hcc')))
                    str_hcc = str(saverecord.hcc_no)
                    length = len(str_hcc)
                    #check for proper length of Hcc_no
                    if length != 9:
                        error = True
                        print('wrong length sadge')
                        messages.error(request, "Specified Healthcard Number is invalid! Please enter a valid Healthcard Number.")
                    else:
                        saverecord.save()
                        #Risk Factor checks
                        saverecord2 = RiskFactor()
                        saverecord2.hcc_no = Civilian.objects.get(hcc_no = int(request.POST.get('hcc_no')))
                        if(request.POST.get('location') == 'Yes'): 
                            saverecord2.location = True
                        else:
                            saverecord2.location = False

                        if(request.POST.get('occupation') == 'Yes'): 
                            saverecord2.occupation = True
                        else:
                            saverecord2.occupation = False

                        if(int (request.POST.get('age')) >=70):
                            saverecord2.at_risk_age = True

                        saverecord2.save()

                        if(request.POST.get('health_condition1')):
                            saverecord3 = HealthCondition()
                            saverecord3.hcc_no = Civilian.objects.get(hcc_no = int(request.POST.get('hcc_no')))
                            saverecord3.condition = request.POST.get('health_condition1')
                            saverecord3.health_condition_id = random.randint(0,10000) #placeholder for now, since I am unsure if the key is automatically generated. 
                            saverecord3.save()

                        if(request.POST.get('health_condition2')):
                            saverecord4 = HealthCondition()
                            saverecord4.hcc_no = Civilian.objects.get(hcc_no = int(request.POST.get('hcc_no')))
                            saverecord4.condition = request.POST.get('health_condition2')
                            saverecord4.health_condition_id = random.randint(0,10000) #placeholder for now, since I am unsure if the key is automatically generated. 
                            saverecord4.save()

        if error == False:
            siteRedirect = '/civilian/' + request.POST.get('hcc_no') + '/'
            return redirect(siteRedirect)

    
    return render(request, "tracker/civilian_registration.html", context_dict)


def newCivilianIntError():
    errorMSG = "Please enter valid INTEGER values into Health Care Number, Phone Number, and Doctor HealthCare Number."
    #send this back to the civilian registration screen 

def civilianAlreadyExists():
    newErrorMSG = "Error, your information already exists in the database. Please login." 

# This endpoint will have to handle a GET and POST request
def edit_civilian(request, hcc_no):
    
    my_civilian = Civilian.objects.get(hcc_no = hcc_no)

    my_doctor = Doctor.objects.get(hcc_no = my_civilian.doctor_hcc.hcc_no)

    context_dict = {
        "civilian_obj": my_civilian,
        "doctor_obj": my_doctor
    }

    if request.method == 'POST':
        if (request.POST.get('phone_no') and
            request.POST.get('address') and request.POST.get('age') and request.POST.get('first_name') and
            request.POST.get('last_name') and request.POST.get('doctor_hcc')):

            my_civilian.phone_no = int(request.POST.get('phone_no')) 
            my_civilian.address = request.POST.get('address')
            my_civilian.age = int(request.POST.get('age'))
            my_civilian.first_name = request.POST.get('first_name')
            my_civilian.last_name = request.POST.get('last_name')
            my_civilian.doctor_hcc = Doctor.objects.get(hcc_no = int (request.POST.get('doctor_hcc')))
            my_civilian.save()     

        siteRedirect = '/civilian/' + str(my_civilian.hcc_no) + '/'
        return redirect(siteRedirect)

    else:    
        return render(request, "tracker/edit_civilian.html", context_dict)
    

def civilian_riskfactor(request, hcc_no):
    try:
        my_riskfactor = RiskFactor.objects.get(hcc_no = hcc_no)
        context = {
            "my_riskfactor": my_riskfactor,
        }

        return render(request, "tracker/civilian_riskfactor.html", context)
    except RiskFactor.DoesNotExist:
        raise Http404("Risk factor does not exist for this civilian")


def civilian_appointments(request, hcc_no):
    my_appointments = Appointment.objects.filter(civilian_hcc_no = hcc_no)
    my_civilian = Civilian.objects.get(hcc_no = hcc_no)
    
    context = {
        "my_appointments": my_appointments,
        "my_civilian": my_civilian
    }
    return render(request, "tracker/civilian_appointments.html", context)



def add_appointment(request, hcc_no):

    my_civilian = Civilian.objects.get(hcc_no = hcc_no)

    ##if it exists continue
    my_riskfactor = RiskFactor.objects.get(hcc_no = hcc_no)
    ##else default risk factor is 'low'
    

    risk_score = my_riskfactor.get_score()

    datetime_object = datetime.datetime.today()

    three_month = datetime_object + timedelta(days=90) 
    six_month = datetime_object + timedelta(days=180) 

    if(risk_score == 'medium'):
        datetime_object = three_month
        print(datetime_object)
    if(risk_score == 'low'):
        datetime_object = six_month
        print(datetime_object)


    dateStr = datetime_object.strftime("%Y-%m-%d")
    print("Printing the formatted string")
    print(dateStr)

    context_dict = {
        "civilian_obj": my_civilian,
        "vaccine_Sites": VaccinationSite.objects.all(),
        "vaccine_obj" : Vaccine.objects.all(),
        "date_Str": dateStr
    }



    if request.method == 'POST':
        if (request.POST.get('DIN_no') and
            request.POST.get('site_address') and request.POST.get('appointment_date')):
        

            my_appointment = Appointment()
            ##placeholder logic for nurse adding until I can figure out how to handle not null following for loop
            my_appointment.nurse_hcc_no = Nurse.objects.get(hcc_no = 343434343)

            my_appointment.appointment_id = random.randint(0,10000)
            my_appointment.civilian_hcc_no = Civilian.objects.get(hcc_no = hcc_no)
            my_appointment.vaccine_DIN_no = Vaccine.objects.get(DIN_no = request.POST.get('DIN_no')) ##here 
            my_appointment.vaccination_site_address = VaccinationSite.objects.get(address = request.POST.get('site_address'))
            
            my_appointment.time = request.POST.get('appointment_date')
            
            #Later to do - randomly select a nurse in each site rather than the first result in the foor loop
            nurse_obj = Nurse.objects.all()

            for data in nurse_obj: 
                
                if(data.site_address == request.POST.get('site_address')):
                    my_appointment.nurse_hcc_no = Nurse.objects.get(hcc_no = data.hcc_no)
            

            my_appointment.save()
             

        siteRedirect = '/civilian/' + str(my_civilian.hcc_no) + '/'
        return redirect(siteRedirect)

    else: 
        return render(request, "tracker/add_appointment.html", context_dict)


def civilian_doctor(request, hcc_no):
    try:
        my_civilian = Civilian.objects.get(hcc_no = hcc_no)
        my_doctor = Doctor.objects.get(hcc_no = my_civilian.doctor_hcc.hcc_no)
        my_doctor_certifications = DoctorCertification.objects.filter(doctor_hcc_no = my_doctor.hcc_no)
        context = {
            "my_doctor": my_doctor,
            "my_doctor_certifications": my_doctor_certifications,
        }

        return render(request, "tracker/civilian_doctor.html", context)
    except (Civilian.DoesNotExist, Doctor.DoesNotExist):
        raise Http404("Queried objects do not exist")

# Nurse Views: #########################################################
# def nurse_homepage(request, hcc_no):
#    try:
#        my_nurse = Nurse.objects.get(hcc_no = hcc_no)
#    except Nurse.DoesNotExist:
#        raise Http404("Nurse does not exist")
#    return HttpResponse("This is your information %s" % my_nurse)

def nurse_homepage(request, hcc_no):
    try:
        my_nurse = Nurse.objects.get(hcc_no=hcc_no)
        context_dict = {
            "nurse_obj": my_nurse
        }
    except:
        return redirect('/nurse/')
    return render(request, 'tracker/nurse_homepage.html', context_dict)

def nurse_appointments(request, hcc_no):
    my_nurse_appointments = Appointment.objects.filter(nurse_hcc_no=hcc_no)
    context_dict = {
        "nurse_obj": my_nurse_appointments
    }
    return render(request, 'tracker/nurse_appointments.html', context_dict)

def nurse_vaccines(request):
    my_vaccines = Vaccine.objects.filter()
    context_dict = {
        "vaccine_obj": my_vaccines
    }
    return render(request, 'tracker/nurse_vaccines.html', context_dict)

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
    return render(request, 'tracker/nurse_vaccine_details.html', context_dict)

def nurse_ppe(request, hcc_no):
    my_nurse_ppe = Ppe.objects.filter(nurse_hcc=hcc_no)
    context_dict = {
        "nurse_obj": my_nurse_ppe
    }
    return render(request, 'tracker/nurse_ppe.html', context_dict)


# This endpoint will have to handle a GET and POST request
# GET - display the fields that the user needs to fill it
# POST - upon button click, validate the fields and save the new item to the database
def new_nurse(request):

    context_dict = {
        "vaccine_Sites": VaccinationSite.objects.all()
    }


    if request.method == 'POST':

        #future to do: check if they exist in db and return to the registration page. 
        if (request.POST.get('hcc_no') and request.POST.get('phone_no') and request.POST.get('sex') and
            request.POST.get('address') and request.POST.get('age') and request.POST.get('first_name') and
            request.POST.get('last_name') and request.POST.get('site_address')):
                saverecord = Nurse()
                saverecord.hcc_no = int(request.POST.get('hcc_no'))
                saverecord.phone_no = int(request.POST.get('phone_no')) 
                saverecord.sex = request.POST.get('sex')
                saverecord.address = request.POST.get('address')
                saverecord.age = int(request.POST.get('age'))
                saverecord.first_name = request.POST.get('first_name')
                saverecord.last_name = request.POST.get('last_name')
                saverecord.site_address = VaccinationSite.objects.get(address = request.POST.get('site_address'))
                
                saverecord.save()

        siteRedirect = '/nurse/' + request.POST.get('hcc_no') + '/'
        return redirect(siteRedirect)

    else: 
        return render(request, "tracker/nurse_registration.html", context_dict)

# This endpoint will have to handle a GET and POST request
# GET - get the current values of the nurse and display in editable fields
# POST - upon button click, validate fields and update if correct
def edit_nurse(request, hcc_no):
    my_nurse = Nurse.objects.get(hcc_no = hcc_no)
    my_site = VaccinationSite.objects.get(address = my_nurse.site_address.address)

    context_dict = {
        "nurse_obj": my_nurse,
        "vaccine_Sites": VaccinationSite.objects.all()
    }

    if request.method == 'POST':
        if (request.POST.get('phone_no') and
            request.POST.get('address') and request.POST.get('age') and request.POST.get('first_name') and
            request.POST.get('last_name') and request.POST.get('site_address')):

            my_nurse.phone_no = int(request.POST.get('phone_no')) 
            my_nurse.address = request.POST.get('address')
            my_nurse.age = int(request.POST.get('age'))
            my_nurse.first_name = request.POST.get('first_name')
            my_nurse.last_name = request.POST.get('last_name')
            my_nurse.site_address = VaccinationSite.objects.get(address = request.POST.get('site_address'))
            my_nurse.save()     

        siteRedirect = '/nurse/' + str(my_nurse.hcc_no) + '/'
        return redirect(siteRedirect)

    else:    
        return render(request, "tracker/edit_nurse.html", context_dict)


  

# This endpoint will show all disposal sites in the database
def nurse_disposal_sites(request):
    my_disposal_sites = DisposalSite.objects.filter()

    context = {
        "my_disposal_sites": my_disposal_sites
    }

    return render(request, "tracker/nurse_disposal_sites.html", context)

# This endpoint will show all vaccination sites in the database
def nurse_vaccination_sites(request):
    my_vaccination_sites = VaccinationSite.objects.filter()

    context = {
        "my_vaccination_sites": my_vaccination_sites
    }
    
    return render(request, "tracker/nurse_vaccination_sites.html", context)