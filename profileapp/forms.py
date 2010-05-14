from django.forms import ModelForm, TextInput, DateField
from profileapp.models import UserProf


class CalendarWidget (TextInput):
    """ This widget is used to enable JQuery UI datepicker for DateField
    """
    class Media:
        css = {'all':('/css/redmond/jquery-ui-1.8.1.custom.css',)}
        js = ('/js/jquery-1.4.2.min.js',
                '/js/jquery-ui-1.8.1.custom.min.js',
                '/js/init.datepicker.js')


class ProfileForm (ModelForm):
    """ This form is used to change entries in UserProf table"""
    birth_date = DateField(
            widget=CalendarWidget(attrs={'id':'calendar-widget'}))
    class Meta:
        model = UserProf
        fields = ['contacts', 'biography', 'birth_date',
                'last_name', 'first_name']