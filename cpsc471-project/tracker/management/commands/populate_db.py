from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.apps import apps
import csv

from tracker.models import *

def create_vaccination_site(*args):
    VaccinationSite.objects.get_or_create(
        address=args[0],
        capacity=args[1],
        contact_name=args[2],
        contact_phone_no=args[3],
    )

create_function = {
    'vaccinationsite': create_vaccination_site,
}


class Command(BaseCommand):
    help = "Create model objects with the file path specified"

    def handle(self, *args, **options):
        with open("tracker/data/sampledata.csv") as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                try:
                    # Try to get a model that corresponds to the first column in this row
                    apps.get_model('tracker', row[0])

                    # If the model is valid, call the corresponding create function and pass it the rest of the row as arguments 
                    create_function[row[0]](*row[1:])
                    self.stdout.write("created " + row[0] + " successfully")

                except LookupError:
                    self.stderr.write("error: model " + row[0] + " does not exist in tracker.models")
                
