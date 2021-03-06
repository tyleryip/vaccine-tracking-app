import datetime

from django.db import models
from django.db.models import constraints
from django.utils import timezone

# Create your models here.
# Note: Django does not support compound primary keys, so for entities we had
# multiple primary keys as part of a compound key, we create surrogate keys
# and enforced the compound primary key constraint with unique_together metadata

class Vaccine(models.Model):
    DIN_no = models.IntegerField("DIN (Drug Identification Number)", primary_key=True)
    disease_treated = models.CharField(max_length=200)
    recommended_dose = models.CharField(max_length=200)
    expiry_date = models.DateField()
    manufacturer_name = models.CharField(max_length=200)

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "DIN: " + str(self.DIN_no) + " - " + self.disease_treated

class VaccineSideEffect(models.Model):
    vaccine_side_effect_id = models.IntegerField("ID", primary_key=True)
    vaccine_DIN_no = models.ForeignKey(Vaccine, on_delete=models.CASCADE, verbose_name='Vaccine')
    side_effect_name = models.CharField("Side Effect", max_length=200)

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "DIN: " + str(self.vaccine_DIN_no) + " - " +  self.side_effect_name

class VaccinationSite(models.Model):
    address = models.CharField(max_length=200, primary_key=True)
    capacity = models.IntegerField()
    contact_name = models.CharField(max_length=200)
    contact_phone_no = models.IntegerField()

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "Address: " + self.address

class StoredAt(models.Model):
    stored_at_id = models.IntegerField(primary_key=True)
    DIN_no = models.ForeignKey(Vaccine, on_delete=models.CASCADE, verbose_name='Vaccine')
    vaccination_site_address = models.ForeignKey(VaccinationSite, on_delete=models.CASCADE)
    temperature = models.FloatField("Storage Temp (°C)", default=20)
    humidity = models.FloatField('Humidity (%)', default=60)
    lighting = models.FloatField('Light Level (Lumens)', default=0)

    # Metadata for this class
    class Meta:
        verbose_name = 'Vaccine Stockpile (StoredAt)'
        verbose_name_plural = 'Vaccine Stockpiles (StoredAt)'

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "DIN: " + str(self.DIN_no) + " - " + str(self.vaccination_site_address)

class DisposalSite(models.Model):
    address = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    disposal_method = models.CharField(max_length=200)

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "Address: " + self.address

class DisposedAt(models.Model):
    disposed_at_id = models.IntegerField(primary_key=True)
    DIN_no = models.ForeignKey(Vaccine, on_delete=models.CASCADE, verbose_name='Vaccine')
    disposal_site_address = models.ForeignKey(DisposalSite, on_delete=models.CASCADE)
    sharp = models.BooleanField(default=True, verbose_name='Sharp Risk')
    biohazard_leakage = models.BooleanField(default=True, verbose_name='Biohazard Leakage Risk')

    # Metadata for this class
    class Meta:
        verbose_name = 'Vaccine Disposal (DisposedAt)'
        verbose_name_plural = 'Vaccine Disposals (DisposedAt)'

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "Din: " + str(self.DIN_no) + " - Address: " + str(self.disposal_site_address)

class Doctor(models.Model): 
    hcc_no = models.IntegerField("Healthcare Card Number", primary_key=True)
    phone_no = models.IntegerField()
    sex = models.CharField(max_length = 1)
    address = models.CharField(max_length = 200)
    age = models.IntegerField()
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    place_of_practice = models.CharField(max_length = 200)

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "Doctor HCC: " + str(self.hcc_no) + " - " + str(self.first_name) + " " + str(self.last_name)
    
    # Returns the full name of this doctor
    def get_fullname(self):
        return self.first_name + " " + self.last_name

    # Used to describe the function for the admin display
    get_fullname.short_description = 'Full Name'

class Civilian(models.Model):
    hcc_no = models.IntegerField("Healthcare Card Number", primary_key=True)
    phone_no = models.IntegerField("Phone Number")
    sex = models.CharField(max_length=1)
    address = models.CharField(max_length=200)
    age = models.IntegerField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    doctor_hcc = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "Civilian HCC: " + str(self.hcc_no) + " - " + self.first_name + " " + self.last_name

    # Returns the fullname of this civilian
    def get_fullname(self):
        return self.first_name + " " + self.last_name

    # Used to describe the function for the admin display
    get_fullname.short_description = 'Full Name'


class RiskFactor(models.Model):
    hcc_no = models.ForeignKey(Civilian, on_delete=models.CASCADE, primary_key=True)
    location = models.BooleanField("High-Risk Location", default=False)
    occupation = models.BooleanField("High-Risk Occupation (Health Care)", default=False)
    at_risk_age = models.BooleanField("High-Risk Age Bracket (>70)", default=False)

    # Return the risk factor for this civilian based on health conditions and risk assessment questions
    def calculate_riskfactor_score(self):
        conditions = HealthCondition.objects.filter(hcc_no = self.hcc_no)
        score = 0
        # Geometric increase for each additional condition
        for i, condition in enumerate(conditions):
            score += (5 * i)

        score += (self.occupation * 1000) + (self.location * 25) + (self.at_risk_age * 75)
        return score

    # Return the risk factor score in a string format
    def get_score(self):
        score = self.calculate_riskfactor_score()

        if score > 100:
            return "high"
        elif score > 50:
            return "medium"
        else: 
            return "low"

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "HCC: " + str(self.hcc_no)

class HealthCondition(models.Model):
    health_condition_id = models.IntegerField(primary_key=True)
    hcc_no = models.ForeignKey(Civilian, on_delete=models.CASCADE)
    condition = models.CharField(max_length=200)

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "HCC: " + str(self.hcc_no) + " - " + self.condition

class Nurse(models.Model):
    hcc_no = models.IntegerField("Healthcare Card Number", primary_key = True)
    phone_no = models.IntegerField()
    sex = models.CharField(max_length=1)
    address = models.CharField(max_length=200)
    age = models.IntegerField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    site_address = models.ForeignKey(VaccinationSite, on_delete=models.CASCADE)

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "Nurse HCC: " + str(self.hcc_no) + " - " + self.first_name + " " + self.last_name

    # TReturns the full name of this nurse
    def get_fullname(self):
        return self.first_name + " " + self.last_name

    # Used to describe the function for the admin display
    get_fullname.short_description = 'Full Name'

class Appointment(models.Model):
    appointment_id = models.IntegerField(primary_key=True)
    time = models.DateTimeField()
    vaccine_DIN_no = models.ForeignKey(Vaccine, on_delete=models.CASCADE, verbose_name='Vaccine')
    nurse_hcc_no = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    civilian_hcc_no = models.ForeignKey(Civilian, on_delete=models.CASCADE)
    vaccination_site_address = models.ForeignKey(VaccinationSite, on_delete=models.CASCADE, verbose_name='Location')

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "ID: " + str(self.appointment_id) + " - Time: " + str(self.time) + " - Client: " + str(self.civilian_hcc_no)

class DoctorCertification(models.Model):
    doctor_certification_id = models.IntegerField(primary_key=True)
    doctor_hcc_no = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    certification = models.CharField(max_length=200)

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "Doctor HCC: " + str(self.doctor_hcc_no) + " - " + self.certification

class PpeSupplier(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    website = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    contact_phone = models.IntegerField()

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "Supplier Name: " + str(self.name) + " - contact info: " + str(self.contact_phone)

class Ppe(models.Model):
    ppe_id = models.IntegerField(primary_key=True)
    is_disposable = models.BooleanField(default=True)
    supplier_name = models.ForeignKey(PpeSupplier, on_delete=models.CASCADE, verbose_name='Supplier')
    nurse_hcc = models.ForeignKey(Nurse, on_delete=models.CASCADE, verbose_name='Assigned Nurse')

    # toString() function for displaying in the admin site and elsewhere
    def __str__(self):
        return "PPE ID: " + str(self.ppe_id) + " - Manufactured by: " + str(self.supplier_name) + " - Used by: " + str(self.nurse_hcc)