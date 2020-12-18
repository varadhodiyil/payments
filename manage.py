#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payments.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    from django.conf import settings
    if 'test' in sys.argv:
        import logging
        logging.disable(logging.CRITICAL)
        settings.DEBUG = False
        settings.TEMPLATE_DEBUG = False

        settings.DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test_database',
            }
        }
        settings.MIDDLEWARE_CLASSES = [
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ]

    if 'test' in sys.argv and '--time' in sys.argv:
        sys.argv.remove('--time')
        from django import test
        import time

        def setUp(self):
            self.startTime = time.time()

        def tearDown(self):
            total = time.time() - self.startTime
            if total > 0.5:
                print("\n\t\033[91m%.3fs\t%s\033[0m" .format(
                    total, self._testMethodName))

        test.TestCase.setUp = setUp
        test.TestCase.tearDown = tearDown
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
