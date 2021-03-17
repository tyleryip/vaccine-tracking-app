import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Vaccine(models.Model):
    DIN_no = models.IntegerField(primary_key=True)
    disease_treated = models.CharField(max_length=200)
    recommended_dose = models.CharField(max_length=200)
    expiry_date = models.DateTimeField()
    manufacturer_name = models.CharField(max_length=200)

    def __str__(self):
        return "DIN: " + str(self.DIN_no) + " - " + self.disease_treated

class VaccineSideEffect(models.Model):
    DIN_no = models.ForeignKey(Vaccine, on_delete=models.CASCADE, primary_key=True)
    side_effect_name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return "DIN: " + str(self.DIN_no) + " - " +  self.side_effect_name

class VaccinationSite(models.Model):
    address = models.CharField(max_length=200, primary_key=True)
    capacity = models.IntegerField()
    contact_name = models.CharField(max_length=200)
    contact_phone_no = models.IntegerField()

    def __str__(self):
        return "Address: " + self.address

class StoredAt(models.Model):
    DIN_no = models.ForeignKey(Vaccine, on_delete=models.CASCADE, primary_key=True)
    address = models.ForeignKey(VaccinationSite, on_delete=models.CASCADE, primary_key=True)
    temperature = models.FloatField(default=20)
    humidity = models.FloatField(default=60)
    lighting = models.FloatField(default=0)

    def __str__(self):
        return "DIN: " + str(self.din_no) + " - " + self.site_address

class DisposalSite(models.Model):
    address = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    disposal_method = models.CharField(max_length=200)

    def __str__(self):
        return "Address: " + self.address
class DisposedAt(models.Model):
    DIN_no = models.ForeignKey(Vaccine, on_delete=models.CASCADE, primary_key=True)
    address = models.ForeignKey(DisposalSite, on_delete=models.CASCADE, primary_key=True)
    sharp = models.BooleanField(default=True)
    biohazard_leakage = models.BooleanField(default=True)

    def _str__(self):
        return "Din: " + str(self.DIN_no) + " - Address: " + str(self.site_address)

class Doctor(models.Model): 
    hcc_no = models.IntegerField(primary_key=True)
    phone_no = models.IntegerField()
    sex = models.CharField(max_length = 1)
    address = models.CharField(max_length = 200)
    age = models.IntegerField()
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    place_of_practice = models.CharField(max_length = 200)

    def __str__(self):
        return "Doctor HCC: " + str(self.hcc_no) + " - " + str(self.firstName) + " " + str(self.lastName)

class Civilian(models.Model):
    hcc_no = models.IntegerField(max_length=9, primary_key=True)
    phone_no = models.IntegerField()
    sex = models.CharField(max_length=1)
    address = models.CharField(max_length=200)
    age = models.IntegerField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    doctor_hcc = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return "Civilian HCC: " + str(self.hcc_no) + " - " + self.firstName + " " + self.lastName

class RiskFactor(models.Model):
    hcc_no = models.ForeignKey(Civilian, on_delete=models.CASCADE, primary_key=True)
    location = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200)
    at_risk_age = models.BooleanField()

    def __str__(self):
        return "HCC: " + str(self.hcc_no)

class HealthCondition(models.Model):
    hcc_no = models.ForeignKey(Civilian, on_delete=models.CASCADE, primary_key=True)
    condition = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return "HCC: " + str(self.hcc_no) + " - " + self.condition

class Nurse(models.Model):
    hcc_no = models.IntegerField(primary_key = True)
    phone_no = models.IntegerField()
    sex = models.CharField(max_length=1)
    address = models.CharField(max_length=200)
    age = models.IntegerField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    site_address = models.ForeignKey(VaccinationSite, on_delete=models.CASCADE)

    def __str__(self):
        return "Nurse HCC: " + str(self.hcc_no) + " - " + self.firstName + " " + self.lastName

class Appointment(models.Model):
    appointment_id = models.IntegerField(primary_key=True)
    time = models.DateTimeField()
    vaccine_DIN_no = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    nurse_hcc_no = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    civilian_hcc_no = models.ForeignKey(Civilian, on_delete=models.CASCADE)
    site_address = models.ForeignKey(Vaccine, on_delete=models.CASCADE)

class DoctorCertification(models.Model):
    doctor_hcc_no = models.ForeignKey(Doctor, on_delete=models.CASCADE, primary_key=True)
    certification = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return "Doctor HCC: " + str(self.doctor_hcc_no) + " - " + self.certification

class PpeSupplier(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    website = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    contact_phone = models.IntegerField()

    def __str__(self):
        return "Supplier Name: " + str(self.name) + " - contact info: " + str(self.contact_phone)

class Ppe(models.Model):
    ppe_id = models.IntegerField(max_length=9, primary_key=True)
    is_disposable = models.BooleanField()
    supplier_name = models.ForeignKey(PpeSupplier, on_delete=models.CASCADE)
    nurse_hcc = models.ForeignKey(Nurse, on_delete=models.CASCADE)

    def __str__(self):
        return "PPE ID: " + str(self.ppe_id) + " - Manufactured by: " + str(self.supplier_name) + " - Used by: " + str(self.nurse_hcc)