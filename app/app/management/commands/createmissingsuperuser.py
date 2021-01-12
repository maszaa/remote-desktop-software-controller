from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create superuser if one does not already exist"

    def handle(self, *args, **options):
        if get_user_model().objects.filter(is_superuser=True).exists() is False:
            call_command("createsuperuser")
        else:
            print("Superuser exists")
