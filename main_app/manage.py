#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
# from views

def main():
    """Run administrative tasks."""
    # views.model = get_kandinsky2('cuda', task_type='text2img', cache_dir='/img', model_version='2.1',
    #                        use_flash_attention=False)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
