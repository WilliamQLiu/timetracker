import datetime
import pdb

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _  # customize field names
from django.forms.formsets import formset_factory  # Work with multiple forms on same page
from django.forms.models import modelformset_factory  # Creates formset for specific Model
from django.forms.models import inlineformset_factory # For inline forms
from django.forms.models import modelform_factory
from django.forms.models import BaseModelFormSet
from .models import Time, Program, CostCode


class EncryptInput(forms.Form):
    """ Enter Data to be encrypted """
    raw_message = forms.CharField(max_length=255)


class DateInput(forms.DateInput):
    # Used to create a custom widget for selecting time as date instead of text
    input_type = 'date'


class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ['date_select']  # Explicitly list only these fields
        date_select = forms.DateField()


class ProgramForm(forms.ModelForm):

    # Only allow active programs
    program_select = forms.ModelChoiceField(queryset=CostCode.objects.filter(active=1).select_related('program__program_select'))
    
    class Meta:
        model = Program
        fields = ['program_select', 'hours_spent', 'minutes_spent', 'notes']
        #program_select = forms.ModelChoiceField(queryset=Program.objects.select_related('CostCode').filter(active=1))
        widgets = {
            'notes': forms.Textarea(attrs={'cols': 45, 'rows': 1}),
        }
        help_texts = {
            'hours_spent': _('(For Sick and Vacation, ignore this)'),
            'minutes_spent': _('(For Sick and Vacation, ignore this)'),
        }
        error_messages = {
            'notes': {
                'max_length': _('This note is too long, please shorten.'),
            },
        }
        #exclude = ('time', )  # returns error since its a foreignkey
        #widgets = {'entertime': forms.HiddenInput}

    def clean(self):
        """ Gives us access to the cleaned data """
        cleaned_data = super(ProgramForm, self).clean()
        program_select = self.cleaned_data.get('program_select')
        hours_spent = self.cleaned_data.get('hours_spent')
        minutes_spent = self.cleaned_data.get('minutes_spent')
        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())  # Hide text

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


### For DateRangeForm
def start_date_format():
    """ Take one week ago, convert to string, reformat and return """
    now = datetime.datetime.now() + datetime.timedelta(days=-7)
    str_date = datetime.datetime.strftime(now, '%m/%d/%Y')
    return str_date


def end_date_format():
    """ Take current datetime, convert to string, reformat and return """
    now = datetime.datetime.now()
    str_date = datetime.datetime.strftime(now, '%m/%d/%Y')
    return str_date


class DateRangeForm(forms.Form):
    """ Used for reporting filters of start and end time """
    start_date = forms.DateField(initial = start_date_format())
    end_date = forms.DateField(initial = end_date_format())
    CHOICES = (('1', 'Percent',), ('2', 'Minutes',))
    percentage = forms.ChoiceField(initial='1', widget=forms.RadioSelect, choices=CHOICES)
    #user = forms.ModelChoiceField(queryset=User.objects.values('username'),
    #                              empty_label='All')
    #user = forms.ChoiceField()

TimeFormSet = modelformset_factory(Time)
ProgramFormSet = modelformset_factory(Program)
