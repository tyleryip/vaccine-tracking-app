from django.contrib import admin

# Register your models here.

# Import all (*) from tracker.models
from .models import *

# Registering all models under the admin user (so the admin user can edit them from the admin site)
