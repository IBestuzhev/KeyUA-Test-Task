from django.conf import settings
def process_settings (request):
    return {'global_settings':settings}