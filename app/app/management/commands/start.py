import waitress
from django.core.management.base import BaseCommand

from app.wsgi import application


class Command(BaseCommand):
    help = "Start RDSC server"

    def add_arguments(self, parser):
        parser.add_argument("listen_ip", type=str)
        parser.add_argument("listen_port", type=int)
        parser.add_argument("threads", type=int)

    def handle(self, *args, **options):
        waitress.serve(
            application,
            host=options.get("listen_ip"),
            port=options.get("listen_port"),
            threads=options.get("threads"),
        )
