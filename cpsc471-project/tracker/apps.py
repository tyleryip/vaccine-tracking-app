from django.apps import AppConfig

# Set the config up so the project can find and run this app.
class TrackerConfig(AppConfig):
    name = 'tracker'
    verbose_name = 'Vaccine Tracking Application'

