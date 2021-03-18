from django.contrib import admin

# Register your models here.

# Import all (*) from tracker.models
from .models import Vaccine, VaccineSideEffect, VaccinationSite, StoredAt, DisposalSite, DisposedAt, Doctor, Civilian, RiskFactor, HealthCondition, Nurse, Appointment, DoctorCertification, PpeSupplier, Ppe

# Registering all models under the admin user (so the admin user can edit them from the admin site)
admin.site.register(Vaccine)
admin.site.register(VaccineSideEffect)
admin.site.register(VaccinationSite)
admin.site.register(StoredAt)
admin.site.register(DisposalSite)
admin.site.register(DisposedAt)
admin.site.register(Doctor)
admin.site.register(Civilian)
admin.site.register(RiskFactor)
admin.site.register(HealthCondition)
admin.site.register(Nurse)
admin.site.register(Appointment)
admin.site.register(DoctorCertification)
admin.site.register(PpeSupplier)
admin.site.register(Ppe)
