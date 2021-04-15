from django.contrib import admin

# Import all (*) from tracker.models
from .models import Vaccine, VaccineSideEffect, VaccinationSite, StoredAt, DisposalSite, DisposedAt, Doctor, Civilian, RiskFactor, HealthCondition, Nurse, Appointment, DoctorCertification, PpeSupplier, Ppe

# In general, all ModelAdmin classes below allow the admin site control over the model's table in the database.

# Any of the classes that extend from admin.TabularInline allow for related models to be modified with their
# parent model. Ex. VaccineSideEffects can be added/removed/modified from their parent Vaccine.

# list_display simply allows for manual control over which attribtues are displayed, and in what order.
# inlines attaches any inline classes to that parent class.

class VaccineSideEffectInline(admin.TabularInline):
    model = VaccineSideEffect
    extra = 3

class StoredAtInline(admin.TabularInline):
    model = StoredAt
    extra = 1

class VaccineAdmin(admin.ModelAdmin):
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
    list_display = ('stored_at_id', 'DIN_no', 'vaccination_site_address', 'temperature', 'humidity', 'lighting')

class DisposalSiteAdmin(admin.ModelAdmin):
    list_display = ('address', 'name', 'disposal_method')

class DisposedAtAdmin(admin.ModelAdmin):
    list_display = ('disposed_at_id', 'DIN_no', 'disposal_site_address', 'sharp', 'biohazard_leakage')

class PpeAdmin(admin.ModelAdmin):
    list_display = ('ppe_id', 'is_disposable', 'supplier_name', 'nurse_hcc')

class PpeSupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'contact_name', 'contact_phone')

# Registering all models under the admin user (so the admin user can edit them from the admin site)
admin.site.register(Vaccine, VaccineAdmin)
admin.site.register(Civilian, CivilianAdmin)
admin.site.register(Nurse, NurseAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(VaccinationSite, VaccinationSiteAdmin)
admin.site.register(StoredAt, StoredAtAdmin)
admin.site.register(DisposalSite, DisposalSiteAdmin)
admin.site.register(DisposedAt, DisposedAtAdmin)
admin.site.register(PpeSupplier, PpeSupplierAdmin)
admin.site.register(Ppe, PpeAdmin)

# The entities should not be directly editable
'''
admin.site.register(HealthCondition)
admin.site.register(VaccineSideEffect)
admin.site.register(DoctorCertification)
admin.site.register(RiskFactor)
'''