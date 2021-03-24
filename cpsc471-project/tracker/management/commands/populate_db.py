from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

# Used to process the data stored in our csv file
import csv

# Import the models so we can create them here
from tracker.models import *


### FUNCTIONS TO CREATE MODELS ###

def create_Vaccine(*args):
    try:  
        model, created = Vaccine.objects.get_or_create(
            DIN_no = args[0],
            disease_treated = args[1],
            recommended_dose = args[2],
            expiry_date = args[3],
            manufacturer_name = args[4],
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_VaccineSideEffect(*args):
    try:  
        # We need to retrieve any objects that this object will reference
        vaccine_ref = Vaccine.objects.get(DIN_no = args[1])

        model, created = VaccineSideEffect.objects.get_or_create(
            vaccine_side_effect_id = args[0],
            vaccine_DIN_no = vaccine_ref,
            side_effect_name = args[2],
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # vV

    except Vaccine.DoesNotExist:
        return(-2) # Invalid with status code -2 (Referenced object does not exist)
    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_VaccinationSite(*args):
    try:  
        model, created = VaccinationSite.objects.get_or_create(
            address = args[0],
            capacity = args[1],
            contact_name = args[2],
            contact_phone_no = args[3],
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_StoredAt(*args):
    try:  
        vaccine_ref = Vaccine.objects.get(DIN_no = args[1])
        vaccination_site_ref = VaccinationSite.objects.get(args[2])

        model, created = StoredAt.objects.get_or_create(
            stored_at_id = args[0],
            DIN_no = vaccine_ref,
            vaccination_site_address = vaccination_site_ref,
            temperature = args[3],
            humidity = args[4],
            lighting = args[5],
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except (Vaccine.DoesNotExist, VaccinationSite.DoesNotExist):
        return(-2) # Invalid with status code -2 (Referenced object does not exist)
    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_DisposalSite(*args):
    try:  
        model, created = DisposalSite.objects.get_or_create(
            address = args[0],
            name = args[1],
            disposal_method = args[2]
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_DisposedAt(*args):
    try:  
        vaccine_ref = Vaccine.objects.get(DIN_no = args[1])
        disposal_site_ref = DisposalSite.objects.get(args[2])

        model, created = DisposedAt.objects.get_or_create(
            disposed_at_id = args[0],
            DIN_no = vaccine_ref,
            disposal_site_address = disposal_site_ref,
            sharp = args[3],
            biohazard_leakage = args[4],
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except (Vaccine.DoesNotExist, DisposalSite.DoesNotExist):
        return(-2) # Invalid with status code -2 (Referenced object does not exist)
    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_Doctor(*args):
    try:  
        model, created = Doctor.objects.get_or_create(
                hcc_no = args[0],
                phone_no = args[1],
                sex = args[2],
                address = args[3],
                age = args[4],
                first_name = args[5],
                last_name = args[6],
                place_of_practice = args[7]
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_Civilian(*args):
    try:  
        doctor_ref = Doctor.objects.get(hcc = args[7])

        model, created = Civilian.objects.get_or_create(
            hcc_no = args[0],
            phone_no = args[1],
            sex = args[2],
            address = args[3],
            age = args[4],
            first_name = args[5],
            last_name = args[6],
            doctor_hcc = doctor_ref
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except (Doctor.DoesNotExist):
        return(-2) # Invalid with status code -2 (Referenced object does not exist)
    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_RiskFactor(*args):
    try:  
        civilian_ref = Civilian.objects.get(hcc = args[0])

        model, created = RiskFactor.objects.get_or_create(
            hcc_no = civilian_ref,
            location = args[1],
            occupation = args[2],
            at_risk_age = args[3],
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except (Civilian.DoesNotExist):
        return(-2) # Invalid with status code -2 (Referenced object does not exist)
    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_HealthCondition(*args):
    try:  
        civilian_ref = Civilian.objects.get(hcc = args[1])

        model, created = RiskFactor.objects.get_or_create(
            health_condition_id = args[0],
            hcc_no = civilian_ref,
            condition = args[2]
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except (Civilian.DoesNotExist):
        return(-2) # Invalid with status code -2 (Referenced object does not exist)
    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_Nurse(*args):
    try:  
        vaccination_site_ref = VaccinationSite.objects.get(hcc = args[1])

        model, created = RiskFactor.objects.get_or_create(
            hcc_no = args[0],
            phone_no = args[1],
            sex = args[2],
            address = args[3],
            age = args[4],
            first_name = args[5],
            last_name = args[6],
            site_address = vaccination_site_ref
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except (VaccinationSite.DoesNotExist):
        return(-2) # Invalid with status code -2 (Referenced object does not exist)
    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_Appointment(*args):
    try:  
        vaccine_ref = Vaccine.objects.get(DINO_no = args[2])
        nurse_ref = Nurse.objects.get(hcc = args[3])
        civilian_ref = Civilian.objects.get(hcc = args[4])
        vaccination_site_ref = VaccinationSite.objects.get(hcc = args[5])

        model, created = RiskFactor.objects.get_or_create(
            appointment_id = args[0],
            time = args[1],
            vaccine_DIN_no = vaccine_ref,
            nurse_hcc_no = nurse_ref,
            civilian_hcc_no = civilian_ref,
            vaccination_site_address = vaccination_site_ref
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except (Vaccine.DoesNotExist, Nurse.DoesNotExist, Civilian.DoesNotExist, VaccinationSite.DoesNotExist):
        return(-2) # Invalid with status code -2 (Referenced object does not exist)
    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_DoctorCertification(*args):
    try:  
        doctor_ref = Doctor.objects.get(hcc = args[1])

        model, created = DoctorCertification.objects.get_or_create(
            doctor_certification_id = args[0],
            doctor_hcc = doctor_ref,
            certification = args[2]
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except (Doctor.DoesNotExist):
        return(-2) # Invalid with status code -2 (Referenced object does not exist)
    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_PpeSupplier(*args):
    try:  
        model, created = PpeSupplier.objects.get_or_create(
            name = args[0],
            website = args[1],
            contact_name = args[2],
            contact_phone = args[3],
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)

def create_Ppe(*args):
    try:  
        ppe_supplier_ref = PpeSupplier.objects.get(name = args[2])
        nurse_ref = Nurse.objects.get(hcc = args[3])

        model, created = DoctorCertification.objects.get_or_create(
            ppe_id = args[0],
            is_disposable = args[1],
            supplier_name = ppe_supplier_ref,
            nurse_hcc = nurse_ref
        )
        if(created):
            return(0) # Valid with status code 0 (Object created)
        else:
            return(1) # Valid with status code 1 (Object already exists)

    except (PpeSupplier.DoesNotExist, Nurse.DoesNotExist):
        return(-2) # Invalid with status code -2 (Referenced object does not exist)
    except ValueError:
        return(-1) # Invalid with status code -1 (Invalid parameters or not enough parameters)


# Dictionary to map model names to the create functions
create_function = {
    'Vaccine': create_Vaccine,
    'VaccineSideEffect': create_VaccineSideEffect,
    'VaccinationSite': create_VaccinationSite,
    'StoredAt': create_StoredAt,
    'DisposalSite': create_DisposalSite,
    'DisposedAt': create_DisposedAt,
    'Doctor': create_Doctor,
    'Civilian': create_Civilian,
    'RiskFactor': create_RiskFactor,
    'HealthCondition': create_HealthCondition,
    'Nurse': create_Nurse,
    'Appointment': create_Appointment,
    'DoctorCertification': create_DoctorCertification,
    'PpeSupplier': create_PpeSupplier,
    'Ppe': create_Ppe,
}

# The command class which extends base command, make this python file an executable command
class Command(BaseCommand):
    help = "Create model objects with the file path specified"

    # Business logic for the command, this is what gets executed when the command is called
    def handle(self, *args, **options):
        # Open the csv file
        with open("tracker/data/sampledata.csv") as f:
            reader = csv.reader(f, delimiter=',')
            self.stdout.write("Populating database from provided CSV file...\n--------------------------------------------------------------------")
            # Iterate through the rows
            for index, row in enumerate(reader):
                try:
                    # Try to get a model that corresponds to the first column in this row
                    apps.get_model('tracker', row[0])

                    # If the model is valid, call the corresponding create function and pass it the rest of the row as arguments 
                    result = create_function[row[0]](*row[1:])
                    
                    if(result == 0):
                        # Successfully created model
                        self.stdout.write("row[" + str(index) + "]: " + "successfully created " + row[0])

                    elif(result == -1):
                        # -1 if invalid parameters (not enough or wrong type)
                        self.stdout.write(self.style.ERROR("row[" + str(index) + "]: " + "invalid parameters provided to create " + row[0]))

                    elif(result == 1):
                        # 1 if the model already exists in the database
                        self.stdout.write("row[" + str(index) + "]: \'" + row[0] + "\' model with these attributes already exists")

                    elif(result == -2):
                        # -2 if a referenced model does not exist in the database
                        self.stdout.write(self.style.ERROR("row[" + str(index) + "]: \'" + row[0] + "\' references an object that does not exist"))

                    else:
                        # Unknown status code, just ignore
                        continue

                except LookupError:
                    # If there is an error (model does not exist) write to standard error
                    self.stdout.write(self.style.ERROR("row[" + str(index) + "]: " + "error: model \'" + row[0] + "\' does not exist in tracker.models"))
            
            self.stdout.write("--------------------------------------------------------------------")