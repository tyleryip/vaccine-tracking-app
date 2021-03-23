from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.apps import apps

from tracker.models import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        for model in apps.get_app_config('tracker').get_models():
            model.objects.all().delete()
            self.stdout.write("deleted " + str(model) + " table")