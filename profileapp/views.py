""" Create your views here. """
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from profileapp.models import UserProf
from profileapp.forms import ProfileForm

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
        return redirect('profileapp.views.list_profile', permanent=True)
    return render_to_response ('ShowProfile.html',
                    {'user_prof':user_entry.get_profile()},
                    context_instance=RequestContext(request))


@login_required
def edit_profile (request, user):
    err_msg = profile = None
    if user == request.user.username:
        profile = request.user.get_profile()
    elif request.user.is_staff:
        try:
            profile = User.objects.get(username=user).get_profile()
        except ObjectDoesNotExist:
            err_msg = 'User does not exist'
    else:
        err_msg = "Only staff is allowed to change another users' data"

    if (not err_msg) and request.method == 'POST':
        try:
            ProfileForm(request.POST, instance=profile).save()
        except ValueError:
            pass
        else:
            return redirect(profile)
            
    return render_to_response ('EditProfile.html',
                    {'prof_form':ProfileForm(instance=profile),
                     'wrong_user':err_msg},
                    context_instance=RequestContext(request))