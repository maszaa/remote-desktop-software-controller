#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.conf import settings
from django.core.management import call_command
from django.core.management.utils import get_random_secret_key

# Import some 3rd party packages for pyinstaller if it's creating a package
# Otherwise functionalities using these won't work on runtime
if "pyinstaller" in sys.argv[0]:
    import ahk
    import PIL
    import pyautogui
    import pypugjs.ext.django.templatetags
    import whitenoise.middleware
    import win32gui


def start() -> None:
    """
    Function executed if manage.py isn't provided any arguments i.e. subcommand with possible arguments

    Steps to be executed:
    1. Creates settings.SECRET_KEY_FILE if not present yet
    2. Migrates database
    3. Collects static files
    4. Starts interactive createsuperuser if superusers don't exist yet
    5. Starts server at 0.0.0.0:80 with CPU_CORES * 2
    """
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()

    settings.LOGGER.warning(f"{settings.APP_NAME} starting...")

    if os.path.isfile(settings.SECRET_KEY_FILE) is False:
        secret_key = get_random_secret_key()
        with open(settings.SECRET_KEY_FILE, "w") as f:
            f.write(secret_key)
            settings.LOGGER.warning(f"SECRET_KEY_FILE {settings.SECRET_KEY_FILE} CREATED")

    settings.LOGGER.warning("MIGRATE")
    call_command("migrate", interactive=False)

    settings.LOGGER.warning("COLLECTSTATIC")
    call_command("collectstatic", interactive=False)

    settings.LOGGER.warning("CREATEMISSINGSUPERUSER")
    call_command("createmissingsuperuser")

    settings.LOGGER.warning("START")
    call_command("start", "0.0.0.0", 80, os.cpu_count() * 2)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # If manage.py wasn't provided with any arguments, shortcut to starting the server
    if len(sys.argv) == 1:
        start()
    else:
        execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
