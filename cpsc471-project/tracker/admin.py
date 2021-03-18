from django.contrib import admin

# Register your models here.

# Import all (*) from tracker.models
from .models import Vaccine, VaccineSideEffect, VaccinationSite, StoredAt, DisposalSite, DisposedAt, Doctor, Civilian, RiskFactor, HealthCondition, Nurse, Appointment, DoctorCertification, PpeSupplier, Ppe

# This is a class used to determine how the vaccine will be displayed on the admin site
class VaccineAdmin(admin.ModelAdmin):
    # This list display will tell Django to populate the admin site with the following attributes
    list_display = ('DIN_no', 'disease_treated', 'manufacturer_name')

class CivilianAdmin(admin.ModelAdmin):
    list_display = ('hcc_no', 'get_fullname')

# Registering all models under the admin user (so the admin user can edit them from the admin site)
admin.site.register(Vaccine, VaccineAdmin)
admin.site.register(Civilian, CivilianAdmin)

admin.site.register(VaccineSideEffect)
admin.site.register(VaccinationSite)
admin.site.register(StoredAt)
admin.site.register(DisposalSite)
admin.site.register(DisposedAt)
admin.site.register(Doctor)
admin.site.register(RiskFactor)
admin.site.register(HealthCondition)
admin.site.register(Nurse)
admin.site.register(Appointment)
admin.site.register(DoctorCertification)
admin.site.register(PpeSupplier)
admin.site.register(Ppe)