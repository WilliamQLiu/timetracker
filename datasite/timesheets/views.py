from __future__ import absolute_import  # Allow explicit relative imports
import datetime
import csv
#import pdb # For Python debugging


import pandas as pd
from django.shortcuts import render, render_to_response, \
    RequestContext  # ,get_object_or_404, get_list_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, UpdateView, \
    DeleteView, View  # CreateView,
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
#from django.core.paginator import Paginator  # For Pagination of ListView

 # Django REST Framework API
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from timesheets.serializers import DataSerializer
from timesheets.models import Program

#from rest_pandas import PandasView # For 'django-pandas' library

from timesheets.serializers import UserSerializer, DataSerializer, \
    TimeSerializer, CostCodeSerializer, UserProfileSerializer, ProgramSerializer
from .models import Program, Time, CostCode, UserProfile
from .forms import ProgramForm, TimeForm, DateRangeForm, EncryptInput
#from .forms import TimeFormSet, ProgramFormSet, TimesheetFormSet
#from .tasks import hello_tasks
from .calculations import load_json, df_basic_setup, filter_dates, \
    calc_per_num, calc_cleaning, decrypt_salary
from timesheets.encrypt import create_encryption  # ,return_decryption

# Create your views here.
# Views are the contents of a page (while urls.py is what routes the urls here)
# Takes in HttpRequest and returns HttpResponse

### Trying out Class-Based Views
#class SimplestClassView(View):
#    def get(self, request, *args, **kwargs):
#        return HttpResponse("Hello, world")


class LoggedInMixin(object):
    """ Mixin to ensure user is logged in """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class ProgramListView(LoggedInMixin, ListView):
    model = Program
    #hello_tasks()  # Run immediately
    #hello_tasks.delay()  # Run using redis
    template_name = "program_list.html"
    context_object_name = 'programs'
    paginate_by = 8

    def get_success_url(self):
        return reverse('timesheet')

    def get_queryset(self):
        """ Return only times and programs for the current user"""
        times = Time.objects.filter(user_id=self.request.user)
        return Program.objects.select_related('Time') \
            .filter(time_id=times).order_by('-time__date_select')


class ProgramCreateView(LoggedInMixin, View):
    """ Create time using CBV """
    time_form = TimeForm
    program_form = ProgramForm
    template_name = "program_create.html"

    def get(self, request, *args, **kwargs):
        time_form = TimeForm
        program_form = ProgramForm

        return render_to_response("program_create.html",
                                  locals(),
                                  context_instance=RequestContext(request)
                                  )

    def post(self, request, *args, **kwargs):
        tf = self.time_form(request.POST or None)
        pf = self.program_form(request.POST or None)

        if tf.is_valid() and pf.is_valid():
            # Save time_form
            time_form = tf.save(commit=False)
            time_form.user = request.user
            time_form.save()

            # Save program_form
            save_pf = pf.save(commit=False)
            save_pf.time_id = time_form.id
            # Sick time will be counted as 0 hours
            if str(save_pf.program_select) in ['Sick', 'Vacation']:
                save_pf.hours_spent = 0
                save_pf.minutes_spent = 0
                messages.success(request,
                                 'Sick and vacation time ignores time spent')
                #pdb.set_trace()
            else:
                messages.success(request, 'Thanks!')
            save_pf.save()

            return HttpResponseRedirect('')  # Reset form for more data entry


class ProgramUpdateView(LoggedInMixin, UpdateView):
    model = Program
    template_name = "program_update.html"

    def get_success_url(self):
        return reverse('timesheet')

    def get_context_data(self, **kwargs):
        """ Use the same template for Create View and Update View """
        context = super(ProgramUpdateView, self).get_context_data(**kwargs)
        context['action'] = reverse('program-update',
                                    kwargs={'pk': self.get_object().id})
        return context


class ProgramDeleteView(LoggedInMixin, DeleteView):
    model = Program
    template_name = "program_delete.html"

    def get_success_url(self):
        return reverse('timesheet')


def base(request):
    #users = User.objects.filter(is_active=True)
    return render_to_response("base.html",
                              locals(),
                              context_instance=RequestContext(request)
                              )


# Testing - Just a blank page
def blank(request):

    return render_to_response("blank.html",
                              locals(),
                              context_instance=RequestContext(request)
                              )


@login_required
def encrypt(request):

    encrypted_message = ''

    encrypt_form = EncryptInput(request.GET or None)
    #pdb.set_trace()
    if encrypt_form.is_valid():
        message = encrypt_form.cleaned_data['raw_message']
        encrypted_message = create_encryption(message)
        #print encrypted_message
        #decrypted_message = return_decryption(encrypted_message)
        #print decrypted_message

    return render(request,
                  'encrypt.html', {
                      'encrypt_form': encrypt_form,
                      'encrypted_message': encrypted_message
                  })

'''

class EncryptView(LoggedInMixin, FormView):
    template_name = 'encrypt.html'
    form_class = EncryptInput
    success_url = '/'

    def form_valid(self, form):
        return super(EncryptView, self).form_valid(form)
'''


# Return data for reporting
@login_required
def report(request):

    # Filtering Data - Get input from user
    start = datetime.datetime.now() + datetime.timedelta(days=-7)
    end = datetime.datetime.now()
    percent = None
    #username = None
    # if request.method == 'GET': # if form has been submitted
    date_form = DateRangeForm(request.GET or None)  # None means not entered

    if date_form.is_valid():
        start = date_form.cleaned_data['start_date']
        end = date_form.cleaned_data['end_date']
        percent = date_form.cleaned_data['percentage']
        #username = date_form.cleaned_data['user']
        #username = dict(date_form.fields['username'].choices)[username]

    json_data = load_json()  # Loads all JSON data
    df = df_basic_setup(json_data)  # Setup dataframe from JSON data

    date_df = filter_dates(df, start, end)  # Filter out specific dates

    filtered_df = decrypt_salary(date_df)  # Get salaries back

    # Calculations per person
    table_display = calc_per_num(request, filtered_df, percent)

    #table_dept = calc_department(request, filtered_df)  # Calculations for dept
    table_dept = calc_cleaning(filtered_df, 2)  # Calcs for dept

    return render(request, "report.html", {
                  #'test_data_as_json': test_data_as_json,
                  'df': table_display.to_html(),
                  'dept': table_dept.to_html(),
                  'date_form': date_form
                  })


### All download of data

@login_required
def download_summary(request):
    """ Allow user to download summary data as csv """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="timesheetsum.csv"'

    # Get session variable
    table_display = request.session['table_display']
    item = pd.io.json.read_json(table_display)
    item.to_csv(response)

    return response


@login_required
def download_raw(request):
    """ Allow user to download detailed data as csv """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="timesheetraw.csv"'

    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM dataentry.timesheet_summary''')
    data = cursor.fetchall()  # returns as a tuple

    writer = csv.writer(response)
    writer.writerow(['time_id', 'date_select', 'username', 'email',
                    'program_name', 'cost_code', 'hours_spent',
                    'minutes_spent', 'notes', 'total_minutes'])
    for row in data:
        writer.writerow(row)
    return response


### Django REST Framework API
# Create ViewSets in order to keep the logic nicely organized
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ API endpoint that allows users to be viewed or edited."""
    #queryset = User.objects.all()
    queryset = User.objects.select_related()
    serializer_class = UserSerializer


class TimeViewSet(viewsets.ReadOnlyModelViewSet):
    """ API endpoint that allows groups to be viewed or edited."""
    #queryset = Time.objects.all()
    queryset = Time.objects.select_related()
    serializer_class = TimeSerializer


class CostCodeViewSet(viewsets.ReadOnlyModelViewSet):
    """ API endpoint that allows groups to be viewed or edited."""
    #queryset = CostCode.objects.all()
    queryset = CostCode.objects.select_related()
    serializer_class = CostCodeSerializer


class DataViewSet(viewsets.ReadOnlyModelViewSet):
    #queryset = Program.objects.all()
    #serializer_class = ProgramSerializer
    #queryset = Program.objects.all()
    queryset = Program.objects.select_related()
    serializer_class = DataSerializer


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    #queryset = UserProfile.objects.all()
    queryset = UserProfile.objects.select_related()
    serializer_class = UserProfileSerializer


class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Program.objects.select_related()
    serializer_class = ProgramSerializer


'''
# Actual API
class DataList(APIView):
    """ List all the data """
    def get(self, request, format=None):
        mydata = Program.objects.select_related()
        myserializer = DataSerializer(mydata, many=True)
        return Response(myserializer.data)


class DataDetail(APIView):
    """ Retrieve a single data instance """
    def get_object(self, pk):
        try:
            return Program.objects.get(pk=pk)
        except Program.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        mydata = self.get_object(pk)
        myserializer = DataSerializer(mydata)
        return Response(serializer.data)
'''
### End Django REST Framework API
