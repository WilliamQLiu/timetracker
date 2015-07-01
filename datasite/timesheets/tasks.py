""" Celery tasks that can be called """

from dataentry.celery import app
#from timesheets.calculations import load_json, df_basic_setup, filter_dates, calc_per_num, calc_department

@app.task
def hello_tasks(name='timesheets.hello_tasks'):
    """ A regular function or a task that will be called by celery """
    print('Hello World!  This is a celery task')

#@app.task
#def calc(name='timesheets.calcs'):
#    """ Run calculations for timesheet """
#    load_json()


