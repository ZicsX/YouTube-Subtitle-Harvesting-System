#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import atexit
from subprocess import Popen, DEVNULL, STDOUT
from web_interface.settings import WINDOWS, CELERY_CONCURRENCY


def start_service(args):
    return Popen(args, stdout=DEVNULL, stderr=STDOUT)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_interface.settings")

    celery_args = [
        "celery",
        "-A",
        "web_interface",
        "worker",
        "--logfile=logs/celery.log",
    ]

    if WINDOWS:
        celery_args.extend(["--pool=solo"])

    else:
        if CELERY_CONCURRENCY:
            celery_args.extend(["--concurrency", str(CELERY_CONCURRENCY)])

    #  Start celery worker
    celery_process = start_service(celery_args)

    def exit_handler():
        """Stop the Celery worker and set is_running to False."""

        if WINDOWS:
            if celery_process.poll() is None:
                celery_process.terminate()
                celery_process.wait()
        else:
            os.system("pkill -f 'celery'")

        from harvester.utils.cache_utils import set_system_state

        set_system_state(False)

    atexit.register(exit_handler)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
