""" Context processors are used to add some data to context while
rendering template

"""
from django.conf import settings


def process_settings (request):
    """context processor that add django.conf.settings to context"""
    provide_settings = getattr(settings, 'TEMPLATE_PROVIDE_SETTINGS', False)
    if provide_settings and isinstance(provide_settings, (list, tuple)):
        copy_settings = {}
        for option in provide_settings:
            copy_settings[option] = getattr(settings, option, None)
        return {'global_settings':copy_settings}
    else:
        return {'global_settings':settings}