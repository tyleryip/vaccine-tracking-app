from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

# Import the models
from tracker.models import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        for model in apps.get_app_config('tracker').get_models():
            model.objects.all().delete()
            self.stdout.write("cleared " + str(model) + " table in the local database")