from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

class Command(BaseCommand):
    help = "Create model objects with the file path specified"

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="file path")
        parser.add_argument('--model', type=str, help="model name")

    def handle(self, *args, **options):
        filepath = options['path']
        model_name = options['model']
        model = apps.get_model('tracker', model_name)
        self.stdout.write(str(model))
        self.stdout.write("Called this custom command in tracker!")