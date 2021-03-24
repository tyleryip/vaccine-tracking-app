from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

# Import the models
from tracker.models import *

# This command will clear the database
class Command(BaseCommand):
    help = "will delete all models stored in the tracker database"

    def handle(self, *args, **options):
        for model in apps.get_app_config('tracker').get_models():
            model.objects.all().delete()
            self.stdout.write("cleared " + str(model) + " table in the local database")