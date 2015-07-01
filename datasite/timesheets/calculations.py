from __future__ import absolute_import  # Allow explicit relative imports
import json
from urllib2 import Request, urlopen
import pdb
import requests
from django.conf import settings  # To determine if debug or not
import pandas as pd
import numpy as np

from rest_framework.renderers import JSONRenderer
from timesheets.encrypt import return_decryption


def load_json():
    """ Load data from JSON """
    print "Loading Data From JSON"
    if settings.DEBUG is True:
        #myrequest = Request('http://127.0.0.1:8000/data/?format=json')  # Debug
        URL = "http://127.0.0.1:8000/data/?format=json"
    else:
        #myrequest = Request('http://10.1.1.7/data/?format=json') # Live
        URL = "http://10.1.1.7/data/?format=json"  # Live

    # Old Method
    #response = urlopen(myrequest)
    #raw_data = response.read()
    #return pd.io.json.json_normalize(json.loads(raw_data))
    #pdb.set_trace()

    # New Method - Allows to keep alive forever
    r = requests.get(URL, timeout=None)
    # Breaks nested JSON to a single layer
    return pd.io.json.json_normalize(r.json())


def df_basic_setup(data):
    """ Setup Pandas Dataframe from JSON data """
    df = pd.DataFrame(data, columns=['time.user.username', 'time.date_select',
                      'time.user.userprofile.department.name',
                      'time.user.userprofile.salary',
                      'program_select.program_name', 'hours_spent',
                      'minutes_spent'])
    df.rename(columns={'time.user.username': 'username',
                       'time.date_select': 'date',
                       'program_select.program_name': 'program_name'},
              inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort(columns='date')
    return df


def filter_dates(df, start, end):
    """ Filter df with specific dates """

    # Filter Username
    #if username is not None or 'All':
    #    ''' Filter by Username '''
    #    df = df[df.username==username]

    return df[(df['date'] >= start) & (df['date'] <= end)]  # User Input df


def decrypt_salary(df):
    """ Decrypt salary to determine actual salary """
    #message = "HnxgVm2KwUbnu2fZzZzT5ZtRcjNf1VY8rlpEEQ+VFfQ="
    try:
        df['time.user.userprofile.salary'].fillna('OCGliG48mcTXjARKUg6FeJtRcjNf1VY8rlpEEQ+VFfQ=', inplace=True) # Replace NaN with 0
        df['time.user.userprofile.salary'] = df['time.user.userprofile.salary'].map(lambda x: return_decryption(x))
        df['time.user.userprofile.salary'] = df['time.user.userprofile.salary'].astype('float')
    except:
        print "Error with one of the salaries"
        #pd.set_option('display.max_rows', 500)
        #pd.set_option('display.max_columns', 500)
        #pd.set_option('display.width', 10000)
        pass
        #print df
    #print df.dtypes
    #print return_decryption(df['time.user.userprofile.salary'][3])
    return df


def calc_cleaning(df_calc, option=1):
    """ Take data, clean it, return for calculations
        option=1 means total minutes in raw or percent
        option=2 means for salaries
     """
    df_calc.fillna(0, inplace=True)  # Replace NaN with 0 for calcs
    df_calc['total_time'] = ((df_calc['hours_spent'] * 60)
                             + df_calc['minutes_spent'])
    df_calc['username'] = df_calc['username'].apply(
        lambda x: x.lower())

    if option == 1:  # General, returns total minutes (raw or percent)
        table = pd.pivot_table(df_calc, values=['total_time'],
                               rows=['username'],
                               columns=['program_name'],
                               aggfunc=np.sum, margins=True)  # Pivot data
        return table.total_time

    else:  # option == 2
        # For salary
        df_calc['hourly_wage'] = df_calc[['time.user.userprofile.salary']] / 52 / 35  # Annual to Hourly
        df_calc.rename(columns={'time.user.userprofile.department.name': 'dept'},
                       inplace=True)
        df_calc['cost'] = ((df_calc['total_time'] / 60) *
                           df_calc['hourly_wage'])  # Cost by dep
        df_calc['cost'] = ((df_calc['total_time'] / 60) *
                           df_calc['hourly_wage'])
        table = pd.pivot_table(df_calc, values=['cost'], rows=['dept'],
                               columns=['program_name'], aggfunc=np.sum,
                               margins=True)
        return table


def calc_per_num(request, df_calc, percent):
    """ Take request, dataframe, and calculate percents (default)
        or numbers (percent=2) for each person """
    pd.options.display.float_format = '{:,.0f}'.format
    # Percents and Numbers
    try:
        temp_table = calc_cleaning(df_calc, 1)
        # Iterate through columns except last ('All') and replace value with %
        for x in range(len(temp_table.columns)-1):
            temp_table.iloc[:,x] = ((temp_table.iloc[:,x]/temp_table['All']) * 100)
        temp_table.fillna(0, inplace=True)  # Replace NaNs with 0's
        temp_table.drop('All', axis=1, inplace=True)  # Drop last column
        request.session['table_display'] = temp_table.to_json()

        # Revert back to raw numbers
        if percent == '2':
            temp_table = calc_cleaning(df_calc, 1)
            request.session['table_display'] = temp_table.to_json()

    except:
        # Catch where dataframe is nothing
        temp_table = pd.DataFrame({'Empty': ['No data entered for this timeframe']})

    return temp_table


