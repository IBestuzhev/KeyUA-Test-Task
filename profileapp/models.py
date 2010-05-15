"""This module provides standart Django ORM """
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

# Create your models here.

class UserProf (models.Model):
    """ This table is used to store additional information about users.
    Fields first_name and last_name are duplicates, but I use it to
    build forms with ModelForm and to separate user data from
    login credentials
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    biography = models.TextField()
    contacts = models.TextField()

    user = models.ForeignKey(User, unique=True, editable=False)

    @models.permalink
    def get_absolute_url (self):
        """ Renders an absolute url to view this user's profile """
        return ('profileapp.views.show_profile', (),
                {'user':self.user.username})
    def __unicode__(self):
        return u"%s %s"%(self.first_name, self.last_name)


class LogDB (models.Model):
    """ This table is used to log events to database. """
    TYPE_CHOICES = (
        ('HR','HTTP Request'),
        ('DC','Database entry created'),
        ('DD','Database entry deleted'),
        ('DE','Database entry edited'),
    )
    event_time = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(choices=TYPE_CHOICES, max_length=2)
    info = models.TextField()


def log_handler (signal_type, sender, **kwargs):
    """ creates a note in database when every model is
    creating/editing/deleting
    It does not log LogDB table to avoid recursion
    """
    if sender != LogDB:
        LogDB(event_type=signal_type,
                info="%s model changed with new entry %s"%(
                        sender.__name__,
                        kwargs['instance'])
        ).save()

def del_handler(sender, **kwargs):
    """ Handler for post_delete signal
    It invokes log_handler with signal_type=DD
    """
    return log_handler ('DD', sender, **kwargs)

def save_handler(sender, **kwargs):
    """ Handler for post_save signal
    It invokes log_handler with signal_type=DC or DE depending on
    whether new entry was created or not
    """
    if kwargs['created']:
        return log_handler ('DC', sender, **kwargs)
    else:
        return log_handler ('DE', sender, **kwargs)

post_save.connect(save_handler, dispatch_uid='profileapp.models.post_save')
post_delete.connect(del_handler, dispatch_uid='profileapp.models.post_delete')