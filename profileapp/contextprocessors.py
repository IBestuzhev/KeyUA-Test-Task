""" Context processors are used to add some data to context while
rendering template

"""
from django.conf import settings


def process_settings (request):
    """context processor that add django.conf.settings to context"""
    return {'global_settings':settings}