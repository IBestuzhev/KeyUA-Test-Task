""" This is a middleware module for logging """
from profileapp.models import LogDB
from django.http import HttpResponse
from django.contrib.auth.decorators import _CheckLogin


class LogMiddleware (object):
    """ Middleware class that processes all views """
    def process_view(self, request, view_func, view_args, view_kwargs):
        """ This method captures all calls to view functions
        and saves them to the LogDB table in the database
        """

        # Get undecorated function for require_login decorator
        if (isinstance(view_func,_CheckLogin)):
            view_func = view_func.view_func

        func_name = '.'.join((view_func.__module__, view_func.func_name))
        func_args = [','.join(view_args)]
        if func_args[0]:
            func_args.append(', ')
        func_args.append(','.join(
                ["%s=%s"%(k, v) for k, v in view_kwargs.items()]))
        LogDB(event_type='HR',
              info="Call to %s (%s)"%(func_name, ''.join(func_args))
              ).save()
        return None