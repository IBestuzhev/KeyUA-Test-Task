"""This module provides standart Django ORM """
from django.db import models
from django.contrib.auth.models import User

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

    user = models.ForeignKey(User, unique=True)

    @models.permalink
    def get_absolute_url (self):
        return ('profileapp.views.show_profile', (), {'user':self.user.username})


class LogDB (models.Model):
    """ This table is used to log events to database. """
    TYPE_CHOICES = (
        ('HR','HTTP Request'),
        ('DS','Database entry saved'),
        ('DD','Database entry deleted'),
        ('DE','Database entry edited'),
    )
    event_time = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(choices=TYPE_CHOICES, max_length=2)
    info = models.TextField()