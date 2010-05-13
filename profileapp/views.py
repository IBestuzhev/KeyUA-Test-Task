""" Create your views here. """
# from django.http import HttpResponse
from django.shortcuts import render_to_response
from profileapp.models import UserProf
from django.contrib.auth.models import User

def list_profile (request):
    """ This view is used to show the list of all possible users """
    return render_to_response('ListProfile.html',
                              {'user_list':UserProf.objects.all()})


def show_profile (request, user):
    """ This view shows some information about selected user"""
    return render_to_response ('ShowProfile.html',
                    {'user':User.objects.get(username=user).get_profile()})