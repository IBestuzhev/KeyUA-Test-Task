""" This module provides modellist management command
use
>   python manage.py modellist [APPS]
to run it
"""
from django.core.management.base import BaseCommand
from django.db.models import get_models, get_app
from django.conf import settings

class Command (BaseCommand):
    """ This class is a requirement for management command"""
    help = "Usage: manage.py modellist [APPS]\n \
    Prints all models from selected applications. If no application selected \
    prints all models from settings.INSTALLED_APPS"
    def handle(self, *args, **options):
        """ This method is invoked when you run management commands"""
        app_labels = [app.split('.')[-1] for app in settings.INSTALLED_APPS]
        if not args:
            args = app_labels
        for app in args:
            if app not in app_labels:
                print "%s is not a valid application" % app
                continue

            app_module = get_app(app_label=app, emptyOK=True)
            if app_module is None:
                continue

            print "Models of %s:" % app
            for model in get_models(app_module):
                print " - %s has %d entries" % (
                        model.__name__,
                        model.objects.count()
                )

