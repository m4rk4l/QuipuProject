#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
from os import environ
from pathlib import Path
import sys


def main():
    environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    current_path = Path(__file__).resolve()
    sys.path.append(Path(current_path, 'quipu'))


if __name__ == '__main__':
    main()
