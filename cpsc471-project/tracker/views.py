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

# This function is responsible for the nurse login end point. A nurse will have to pass in their respective health card number
# in order to access their account and its associated information. There is error checking to ensure the health card number is correct,
# and the information in the correct form.
# GET - display the login fields that the nurse has to fill in
# POST - upon button click, the field is validated, and the database returns the entered nurse account
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

# This function is responsible for the civilian login end point. A civilian will have to pass in their respective health card number
# in order to access their account and its associated information. There is error checking to ensure the health card number is correct,
# and the information in the correct form.
# GET - display the login fields that the civilian has to fill in
# POST - upon button click, the field is validated, and the database returns the entered civilian account
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

# This function is responsible for the civilian homepage point. After logging in, the requested account information is 
# displayed with on the page, and multiple buttons are displayed for the civilian to access different features. 
# GET - display the requested civilian information, and display buttons.
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

# This function is repsonsible for the create new civilian end point. A civilian will have to pass in several pieces of info about
#themselves to register. There is error checking to ensure they do not already exist in the database, and to ensure all information entered
#is in the correct format. 
# GET - display the fields that the user needs to fill it
# POST - upon button click, validate the fields and save the new item to the database
@ensure_csrf_cookie
def new_civilian(request):
    
    #the context dictionary passed into the default render
    context_dict = {
        "doctor_obj": Doctor.objects.all(),
    }

    #error checking boolean
    error = False

    #If a civilian has requested to submit their info, the following erorr checking and database injection will occur. 
    if request.method == 'POST':
    
        
        if (request.POST.get('hcc_no') and request.POST.get('phone_no') and request.POST.get('sex') and
            request.POST.get('address') and request.POST.get('age') and request.POST.get('first_name') and
            request.POST.get('last_name') and request.POST.get('doctor_hcc')):
                #Check if the civilian already exists, since we don't want to replace existing data
                try:
                    my_civie = Civilian.objects.get(hcc_no = int(request.POST.get('hcc_no')))

                    error = True
                    messages.error(request, "Account already exists! Please Login with your HealthCard Number.")
                except Civilian.DoesNotExist:
                    #set up a save record to save into the database, and retrieve all the credentials from the post request form.
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
                        #Now establishing a risk factor to inject into the datbase. Such info to consider is if they live in a high risk area or work in a high risk profession. 
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

                        #The first OPTIONAL health condition to insert into the database should they enter anything. 
                        if(request.POST.get('health_condition1')):
                            saverecord3 = HealthCondition()
                            saverecord3.hcc_no = Civilian.objects.get(hcc_no = int(request.POST.get('hcc_no')))
                            saverecord3.condition = request.POST.get('health_condition1')
                            saverecord3.health_condition_id = random.randint(0,10000) 
                            saverecord3.save()

                        #The second OPTIONAL health condition to insert into the database should they enter anything. 
                        if(request.POST.get('health_condition2')):
                            saverecord4 = HealthCondition()
                            saverecord4.hcc_no = Civilian.objects.get(hcc_no = int(request.POST.get('hcc_no')))
                            saverecord4.condition = request.POST.get('health_condition2')
                            saverecord4.health_condition_id = random.randint(0,10000) 
                            saverecord4.save()

        ##if all information is correct, the records are entered into the database and the user is redirected to their homepage. 
        if error == False:
            siteRedirect = '/civilian/' + request.POST.get('hcc_no') + '/'
            return redirect(siteRedirect)

    
    return render(request, "tracker/civilian_registration.html", context_dict)


def newCivilianIntError():
    errorMSG = "Please enter valid INTEGER values into Health Care Number, Phone Number, and Doctor HealthCare Number."
    #send this back to the civilian registration screen 

def civilianAlreadyExists():
    newErrorMSG = "Error, your information already exists in the database. Please login." 

# This function is repsonsible for the editing an existing civilian. A civilian will have to pass in several pieces of info about
#themselves to modify. The HTML info will hold old informaton such that if it is unchanged, it will pass the old info the POST request. 
#A civilian will be unable to change their HCC number information but all other info may be changed. 
# There is error checking to ensure  all information entered is in the correct format. 
# GET - get the current values of the nurse and display in editable fields
# POST - upon button click, validate fields and update if correct
def edit_civilian(request, hcc_no):
    
    my_civilian = Civilian.objects.get(hcc_no = hcc_no)

    my_doctor = Doctor.objects.get(hcc_no = my_civilian.doctor_hcc.hcc_no)

    #the context dictionary to pass into the edit civilian html redirect. 
    context_dict = {
        "civilian_obj": my_civilian,
        "doctor_obj": my_doctor
    }

    #if the civilian submits their changed info, get all changed info and update the db. 
    if request.method == 'POST':
        if (request.POST.get('phone_no') and
            request.POST.get('address') and request.POST.get('age') and request.POST.get('first_name') and
            request.POST.get('last_name') and request.POST.get('doctor_hcc')):

            #set the civilian objects info according to the forms changed info.
            my_civilian.phone_no = int(request.POST.get('phone_no')) 
            my_civilian.address = request.POST.get('address')
            my_civilian.age = int(request.POST.get('age'))
            my_civilian.first_name = request.POST.get('first_name')
            my_civilian.last_name = request.POST.get('last_name')
            my_civilian.doctor_hcc = Doctor.objects.get(hcc_no = int (request.POST.get('doctor_hcc')))
            my_civilian.save()     

            if(request.POST.get('health_condition1')):
                            saverecord3 = HealthCondition()
                            saverecord3.hcc_no = Civilian.objects.get(hcc_no = my_civilian.hcc_no)
                            saverecord3.condition = request.POST.get('health_condition1')
                            saverecord3.health_condition_id = random.randint(0,10000) #placeholder for now, since I am unsure if the key is automatically generated. 
                            saverecord3.save()

            if(request.POST.get('health_condition2')):
                            saverecord4 = HealthCondition()
                            saverecord4.hcc_no = Civilian.objects.get(hcc_no = my_civilian.hcc_no)
                            saverecord4.condition = request.POST.get('health_condition2')
                            saverecord4.health_condition_id = random.randint(0,10000) #placeholder for now, since I am unsure if the key is automatically generated. 
                            saverecord4.save()

        #if info is changed and successfully saved into the db, redirect to the civilians homepage. 
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


#This function is responsible for adding an appointment to an existing civilian in the database. A default request to this endpoint will return a render,
#Redirecting to the add appointment endpoint. It also passes a context dictionary holding information about vaccination sites, vaccines, dates, and your information 
#which is shown on that endpoint in the html. 
# GET - display the fields that the user needs to fill it
# POST - upon button click, validate the fields and save the new item to the database
def add_appointment(request, hcc_no):

    #set up info to be passed into the html endpoint. 
    my_civilian = Civilian.objects.get(hcc_no = hcc_no)
    my_riskfactor = RiskFactor.objects.get(hcc_no = hcc_no)
    risk_score = my_riskfactor.get_score()

    #get todays sdate
    datetime_object = datetime.datetime.today()
    three_month = datetime_object + timedelta(days=90) 
    six_month = datetime_object + timedelta(days=180) 

    #Set future date for vaccination to be dependant on the civilians risk factor score
    if(risk_score == 'medium'):
        datetime_object = three_month
        print(datetime_object)
    if(risk_score == 'low'):
        datetime_object = six_month
        print(datetime_object)

    dateStr = datetime_object.strftime("%Y-%m-%d")

    #the context dictionary to be passed into the end point. 
    context_dict = {
        "civilian_obj": my_civilian,
        "vaccine_Sites": VaccinationSite.objects.all(),
        "vaccine_obj" : Vaccine.objects.all(),
        "date_Str": dateStr
    }

    #once a civilian has submitted their info, the following will do some error checking, and once satasfied, submit the information into the database.
    if request.method == 'POST':
        if (request.POST.get('DIN_no') and
            request.POST.get('site_address') and request.POST.get('appointment_date')):
        
            my_appointment = Appointment()
            
            ##Default nurse if none found in below nurse checking.
            my_appointment.nurse_hcc_no = Nurse.objects.get(hcc_no = 343434343)

            #randomly assign an appointment id 
            my_appointment.appointment_id = random.randint(0,10000)
            #set the hcc number for the appointment to reference the civilian booking it
            my_appointment.civilian_hcc_no = Civilian.objects.get(hcc_no = hcc_no)
            #set the vaccination din number to the vaccine selected
            my_appointment.vaccine_DIN_no = Vaccine.objects.get(DIN_no = request.POST.get('DIN_no')) 
            #set the vaccination site to the selected site. 
            my_appointment.vaccination_site_address = VaccinationSite.objects.get(address = request.POST.get('site_address'))
            #set the appointment time to the selected time 
            my_appointment.time = request.POST.get('appointment_date')

            ##populate an array with ALL Nurses that work at selected site address
            matching_nurses_arr = []
            nurse_obj = Nurse.objects.filter(site_address = request.POST.get('site_address'))

            for data in nurse_obj: 
                    matching_nurses_arr.append(data)

            #randomly select one of the nurses to oversee the appointment       
            arr_len = len(matching_nurses_arr)
            rand_index = random.randint(0, arr_len-1)
            my_appointment.nurse_hcc_no = Nurse.objects.get(hcc_no = matching_nurses_arr[rand_index].hcc_no)

            #save the appointment into the database
            my_appointment.save()
             
        #once an appointment is made, redirect back to the civilians homepage. 
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


# Nurse Views:

# Nurse_homepage is the homepage endpoint for a nurse user and displays button links to other nurse endpoints.
# This endpoint requires a registered nurse's hcc_no to gain access.
# This endpoint will have to handle a GET request.
def nurse_homepage(request, hcc_no):
    try:
        my_nurse = Nurse.objects.get(hcc_no=hcc_no)
        context_dict = {
            "nurse_obj": my_nurse
        }
    except:
        return redirect('/nurse/')
    return render(request, 'tracker/nurse_homepage.html', context_dict)

# Nurse_appointments is the appointments endpoint for a nurse user and displays a list of all the nurse's appointments.
# This endpoint requires a registered nurse's hcc_no to gain access.
# This endpoint will have to handle a GET request.
def nurse_appointments(request, hcc_no):
    my_nurse_appointments = Appointment.objects.filter(nurse_hcc_no=hcc_no)
    context_dict = {
        "nurse_obj": my_nurse_appointments
    }
    return render(request, 'tracker/nurse_appointments.html', context_dict)

# Nurse_vaccines is a vaccine endpoint for a nurse user and displays a list of all available vaccines.
# This endpoint also features button links to see further vaccine details.
# This endpoint will have to handle a GET request.
def nurse_vaccines(request):
    my_vaccines = Vaccine.objects.filter()
    context_dict = {
        "vaccine_obj": my_vaccines
    }
    return render(request, 'tracker/nurse_vaccines.html', context_dict)

# Nurse_vaccine_details is a vaccine endpoint for a nurse user and displays the specifics of a certain vaccine in greater detail.
# The specifics include: basic vaccine information, possible side effect(s), and storage and disposal facility information.
# This endpoint requires a vaccine's unique DIN_no to be specified. 
# This endpoint will have to handle a GET request.
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

# Nurse_ppe is a PPE endpoint for a nurse user and displays a list of all PPE that is being borrowed by the nurse user.
# This endpoint will have to handle a GET request.
def nurse_ppe(request, hcc_no):
    my_nurse_ppe = Ppe.objects.filter(nurse_hcc=hcc_no)
    context_dict = {
        "nurse_obj": my_nurse_ppe
    }
    return render(request, 'tracker/nurse_ppe.html', context_dict)


# This function is repsonsible for the create new nurse end point. A nurse will have to pass in several pieces of info about
#themselves to register. There is error checking to ensure they do not already exist in the database, and to ensure all information entered
#is in the correct format. 


# GET - display the fields that the user needs to fill it
# POST - upon button click, validate the fields and save the new item to the database
@ensure_csrf_cookie
def new_nurse(request):

    #the context dictionary to pass into the new nurse webpage.
    context_dict = {
        "vaccine_Sites": VaccinationSite.objects.all()
    }

    #error checking boolean 
    error = False

    #if the new nurse submits their information then do record saving and error checking.
    if request.method == 'POST':

        #check that all REQUIRED fields are filled out. 
        if (request.POST.get('hcc_no') and request.POST.get('phone_no') and request.POST.get('sex') and
            request.POST.get('address') and request.POST.get('age') and request.POST.get('first_name') and
            request.POST.get('last_name') and request.POST.get('site_address')):
                #Check if nurse already exists, since we don't want to replace existing data
                try:
                    my_nurse = Nurse.objects.get(hcc_no = int(request.POST.get('hcc_no')))
                    error = True
                    messages.error(request, "Account already exists! Please login with your HealthCard Number.")
                except Nurse.DoesNotExist:
                    #create a new record that is a Nurse Object and populate its info with all fields information 
                    saverecord = Nurse()
                    saverecord.hcc_no = int(request.POST.get('hcc_no'))
                    saverecord.phone_no = int(request.POST.get('phone_no')) 
                    saverecord.sex = request.POST.get('sex')
                    saverecord.address = request.POST.get('address')
                    saverecord.age = int(request.POST.get('age'))
                    saverecord.first_name = request.POST.get('first_name')
                    saverecord.last_name = request.POST.get('last_name')
                    saverecord.site_address = VaccinationSite.objects.get(address = request.POST.get('site_address'))
                    #check for correct length of hcc_no
                    str_hcc = str(saverecord.hcc_no)
                    length = len(str_hcc)
                    #check for proper length of Hcc_no
                    if length != 9:
                        error = True
                        print('wrong length inputted')
                        messages.error(request, "Specified Healthcard Number is invalid! Please enter a valid Healthcard Number.")
                    else:
                        saverecord.save()
        #if the nurse has sucessfully been injected into the database, redirect them to their new homepage. 
        if error == False:
            siteRedirect = '/nurse/' + request.POST.get('hcc_no') + '/'
            return redirect(siteRedirect)


    return render(request, "tracker/nurse_registration.html", context_dict)

# This function is repsonsible for the editing an existing nurse. A nurse will have to pass in several pieces of info about
#themselves to modify. The HTML info will hold old informaton such that if it is unchanged, it will pass the old info the POST request. 
#A nurse will be unable to change their HCC number information but all other info may be changed. 
# There is error checking to ensure  all information entered is in the correct format. 

# GET - get the current values of the nurse and display in editable fields
# POST - upon button click, validate fields and update if correct
def edit_nurse(request, hcc_no):
    #get the nurse object from the database
    my_nurse = Nurse.objects.get(hcc_no = hcc_no)
    my_site = VaccinationSite.objects.get(address = my_nurse.site_address.address)

    #The context dictionary containing necessary info to display on the HTML page. 
    context_dict = {
        "nurse_obj": my_nurse,
        "vaccine_Sites": VaccinationSite.objects.all()
    }

    #If a nurse requests to change any info, gather all changed info and update the nurse object in the database. 
    if request.method == 'POST':
        if (request.POST.get('phone_no') and
            request.POST.get('address') and request.POST.get('age') and request.POST.get('first_name') and
            request.POST.get('last_name') and request.POST.get('site_address')):

            #retreieve all fields info and insert it into the Nurse Objects data fields. 
            my_nurse.phone_no = int(request.POST.get('phone_no')) 
            my_nurse.address = request.POST.get('address')
            my_nurse.age = int(request.POST.get('age'))
            my_nurse.first_name = request.POST.get('first_name')
            my_nurse.last_name = request.POST.get('last_name')
            my_nurse.site_address = VaccinationSite.objects.get(address = request.POST.get('site_address'))
            my_nurse.save()     

        #redirect to the nurses homepage once completed. 
        siteRedirect = '/nurse/' + str(my_nurse.hcc_no) + '/'
        return redirect(siteRedirect)

    else:    
        return render(request, "tracker/edit_nurse.html", context_dict)


  
# Nurse_disposal_sites is the disposal site endpoint for a nurse user which displays a list of all the disposal sites in the database.
# This endpoint will have to handle a GET request.
def nurse_disposal_sites(request):
    my_disposal_sites = DisposalSite.objects.filter()

    context = {
        "my_disposal_sites": my_disposal_sites
    }

    return render(request, "tracker/nurse_disposal_sites.html", context)

# Nurse_vaccination_sites is the vaccination site endpoint for a nurse user which displays a list of all the vaccination sites in the database.
# This endpoint will have to handle a GET request.
def nurse_vaccination_sites(request):
    my_vaccination_sites = VaccinationSite.objects.filter()

    context = {
        "my_vaccination_sites": my_vaccination_sites
    }
    
    return render(request, "tracker/nurse_vaccination_sites.html", context)