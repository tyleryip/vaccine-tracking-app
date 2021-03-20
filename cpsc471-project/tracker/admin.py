from django.contrib import admin

# Register your models here.

# Import all (*) from tracker.models
from .models import Vaccine, VaccineSideEffect, VaccinationSite, StoredAt, DisposalSite, DisposedAt, Doctor, Civilian, RiskFactor, HealthCondition, Nurse, Appointment, DoctorCertification, PpeSupplier, Ppe


class VaccineSideEffectInline(admin.TabularInline):
    model = VaccineSideEffect
    extra = 3

class StoredAtInline(admin.TabularInline):
    model = StoredAt
    extra = 1

# This is a class used to determine how the vaccine will be displayed on the admin site
class VaccineAdmin(admin.ModelAdmin):
    # This list display will tell Django to populate the admin site with the following attributes
    list_display = ('DIN_no', 'disease_treated', 'manufacturer_name')
    inlines = [VaccineSideEffectInline, StoredAtInline]

class RiskFactorInline(admin.TabularInline):
    model = RiskFactor
    extra = 1

class HealthConditionInline(admin.TabularInline):
    model = HealthCondition
    extra = 2

class CivilianAdmin(admin.ModelAdmin):
    list_display = ('hcc_no', 'get_fullname', 'sex', 'age')
    inlines = [HealthConditionInline, RiskFactorInline]

class NurseAdmin(admin.ModelAdmin):
    list_display = ('hcc_no', 'get_fullname', 'site_address')

class DoctorCertificationInline(admin.TabularInline):
    model = DoctorCertification
    extra = 2

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('hcc_no', 'get_fullname', 'place_of_practice')
    inlines = [DoctorCertificationInline]

class VaccinationSiteAdmin(admin.ModelAdmin):
    list_display = ('address', 'capacity', 'contact_name', 'contact_phone_no')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('civilian_hcc_no', 'time', 'vaccine_DIN_no', 'vaccination_site_address')

class StoredAtAdmin(admin.ModelAdmin):
    list_display = ('DIN_no', 'vaccination_site_address', 'temperature', 'humidity', 'lighting')

# Registering all models under the admin user (so the admin user can edit them from the admin site)
admin.site.register(Vaccine, VaccineAdmin)
admin.site.register(Civilian, CivilianAdmin)
admin.site.register(Nurse, NurseAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(VaccinationSite, VaccinationSiteAdmin)
admin.site.register(StoredAt, StoredAtAdmin)

# These models do not have rich admin pages yet
admin.site.register(DisposalSite)
admin.site.register(DisposedAt)
admin.site.register(HealthCondition)

admin.site.register(PpeSupplier)
admin.site.register(Ppe)

# The entities should not be directly editable
# admin.site.register(VaccineSideEffect)
# admin.site.register(DoctorCertification)
# admin.site.register(RiskFactor)