""" Create your views here. """
# from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.context import RequestContext
from profileapp.models import UserProf

def list_profile (request):
    """ This view is used to show the list of all possible users """
    return render_to_response('ListProfile.html',
                              {'user_list':UserProf.objects.all()},
                              context_instance=RequestContext(request))


def show_profile (request, user):
    """ This view shows some information about selected user"""
    try:
        user_entry = User.objects.get(username=user)
    except ObjectDoesNotExist:
        return redirect('profileapp.views.list_profile',permanent=True)
    return render_to_response ('ShowProfile.html',
                    {'user':user_entry.get_profile()},
                    context_instance=RequestContext(request))