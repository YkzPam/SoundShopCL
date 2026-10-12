#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soundshop.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver' and os.environ.get('RUN_MAIN') != 'true':
        direccion = '127.0.0.1:8000'
        for argumento in sys.argv[2:]:
            if argumento.isdigit():
                direccion = f'127.0.0.1:{argumento}'
            elif ':' in argumento and argumento.rsplit(':', 1)[-1].isdigit():
                direccion = argumento
        print(f'\nTienda: http://{direccion}/', flush=True)
        print(f'Administrador: http://{direccion}/admin/\n', flush=True)

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
