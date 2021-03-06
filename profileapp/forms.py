from django.forms import ModelForm, TextInput, DateField
from django.utils.datastructures import SortedDict
from profileapp.models import UserProf


class CalendarWidget (TextInput):
    """ This widget is used to enable JQuery UI datepicker for DateField
    """
    class Media:
        css = {'all':('css/redmond/jquery-ui-1.8.1.custom.css',)}
        js = ('js/jquery-1.4.2.min.js',
                'js/jquery-ui-1.8.1.custom.min.js',
                'js/init.datepicker.js')


class ProfileForm (ModelForm):
    """ This form is used to change entries in UserProf table"""
    def __init__ (self, *a, **k):
        """ Invert fields order """
        ModelForm.__init__ (self, *a, **k)
        self.fields = SortedDict(self.fields.items()[::-1])

    birth_date = DateField(
            widget=CalendarWidget(attrs={'id':'calendar-widget'}))
    class Meta:
        model = UserProf