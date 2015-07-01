
# Group By
# Return data for reporting
@login_required
def report(request):

    # Very basic test to send data to template
    #programs = Program.objects.all().select_related('Time').filter(time_id=times).order_by('-time__date_select')
    #test_data_as_json = [1, 2, 3, 4, 5]

    # Read in JSON data, transform into DataFrame, then return DataFrame as HTML
    myrequest = Request('http://127.0.0.1:8000/data/?format=json')
    response = urlopen(myrequest)
    raw_data = response.read()
    data = json.loads(raw_data)
    data = pd.io.json.json_normalize(data) # Breaks up nested JSON to a single layer
    df = pd.DataFrame(data) # Get all fields
    df = pd.DataFrame(data, columns=['time.user.username', 'time.date_select',
                      'time.user.userprofile.department.name',
                      'time.user.userprofile.salary',
                      'program_select.program_name', 'hours_spent', 'minutes_spent'])
    df = df.rename(columns={'time.user.username':'username', 'time.date_select':'date',
                   'program_select.program_name':'program_name'})
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort(columns='date')

    # Filtering Data - Get input from user
    start = datetime.datetime.now() + datetime.timedelta(days=-7) # Form's start date
    end = datetime.datetime.now()
    percent = None
    username = None
    timeframe = None
    #if request.method == 'GET': # if form has been submitted
    date_form = DateRangeForm(request.GET or None) # GET date fields or None for not entered yet

    if date_form.is_valid():
        start = date_form.cleaned_data['start_date']
        end = date_form.cleaned_data['end_date']
        percent = date_form.cleaned_data['percentage']
        timeframe = date_form.cleaned_data['timeframe']
        #username = date_form.cleaned_data['user']
        #username = dict(date_form.fields['username'].choices)[username]

    '''
        if start and end:
               # Start and End Times are valid, filter data to return specific dates
         #all_objects = Program.objects.filter(date_select__gt=start, date_select__lt=end)
            #df = df[(df['date'] > '7/1/2014') & (df['date'] < '7/20/2014')] #works
            #df = df[(df['date'] > '2014-7-1') & (df['date'] < '2014-7-20')] #works
            df = df[(df['date'] >= start) & (df['date'] <= end)] # Filtere dataframe based on user input
        else:
            # Start or End Time is invalid, return all data
            #all_objects = Program.objects.all()
            df = df
    '''

    # Debugging
    #pdb.set_trace()
    df = df[(df['date'] >= start) & (df['date'] <= end)] # Filtere dataframe based on user input

    # Filter Username
    #if username is not None or 'All':
    #    ''' Filter by Username '''
    #    df = df[df.username==username]

    # Percents and Numbers
    try:
        # Data Cleaning
        df_calc = df
        df_calc.fillna(0, inplace=True) # Replace NaN with 0 so we can do calculations
        df_calc['total_time'] = ((df_calc['hours_spent'] * 60) + df_calc['minutes_spent'])
        df_calc['username'] = df_calc['username'].apply(lambda x: x.lower()) # make names lowercase

        # Sum Numbers
        df_calc['month'] = pd.to_datetime(df_calc['date']).map(lambda x: str(x.year)+"-"+str(x.month)) # Get a monthly field
        df_calc['week']= df_calc['date'].map(lambda x: x.isocalendar()[1]) # Get a weekly field

        table = pd.pivot_table(df_calc, values=['total_time'], rows=['username'],
                               columns=['program_name'], aggfunc=np.sum, margins=True) # Pivot data
        table_display = table
        if timeframe == '2':
            # Month
            table = pd.pivot_table(df_calc, values=['total_time'], rows=['month', 'username'],
                               columns=['program_name'], aggfunc=np.sum, margins=True) # Pivot data
        elif timeframe == '3':
            # Weekly
            table = pd.pivot_table(df_calc, values=['total_time'], rows=['week', 'username'],
                               columns=['program_name'], aggfunc=np.sum, margins=True) # Pivot data
        elif timeframe == '4':
            # Daily
            table = pd.pivot_table(df_calc, values=['total_time'], rows=['date', 'username'],
                               columns=['program_name'], aggfunc=np.sum, margins=True) # Pivot data
        else:
            # Shouldn't get here
            pass



        #table.drop('month', axis=1, inplace=True)
        print table_display

        # Get Percentages
        table_pct = table.total_time

        # Iterate through all columns except last ('All'), then replace value with percentage
        for x in range(len(table_pct.columns)-1):
            table_pct.iloc[:,x] = ((table_pct.iloc[:,x]/table_pct['All']) * 100)
        table_pct.fillna(0, inplace=True) # Replace NaNs with 0's
        pd.options.display.float_format = '{:.2f}%'.format # Change display format
        table_pct.drop('All', axis=1, inplace=True) # Drop last column
        table_display = table_pct
        request.session['table_display'] = table_display.to_json() # Save to session variable so can download

        # Revert back to raw numbers
        if percent == '2':
            df_calc = df
            df_calc.fillna(0, inplace=True) # Replace NaN with 0 so we can do calculations
            df_calc['total_time'] = ((df_calc['hours_spent'] * 60) + df_calc['minutes_spent'])
            df_calc['username'] = df_calc['username'].apply(lambda x: x.lower()) # make names lowercase

            # Sum Numbers
            df_calc['month'] = pd.to_datetime(df_calc['date']).map(lambda x: str(x.year)+"-"+str(x.month)) # Get a monthly field
            df_calc['week']= df_calc['date'].map(lambda x: x.isocalendar()[1]) # Get a weekly field
            table = pd.pivot_table(df_calc, values=['total_time'], rows=['username'],
                               columns=['program_name'], aggfunc=np.sum, margins=True) # Pivot data
            pd.options.display.float_format = '{:.1f}'.format # Change display format for number of decimal places
            request.session['table_display'] = table_display.to_json() # Save to session variable so can download


            if timeframe == '2':
                # Month
                table = pd.pivot_table(df_calc, values=['total_time'], rows=['month', 'username'],
                               columns=['program_name'], aggfunc=np.sum, margins=True) # Pivot data
            elif timeframe == '3':
                # Weekly
                table = pd.pivot_table(df_calc, values=['total_time'], rows=['week', 'username'],
                               columns=['program_name'], aggfunc=np.sum, margins=True) # Pivot data
            elif timeframe == '4':
                # Daily
                table = pd.pivot_table(df_calc, values=['total_time'], rows=['date', 'username'],
                               columns=['program_name'], aggfunc=np.sum, margins=True) # Pivot data
            else:
                # Shouldn't get here
                pass

            table_display = table.total_time

    except:
        # Catch where dataframe is nothing
        table_display = pd.DataFrame({'Empty':['No data entered for this timeframe']})

    print table_display


    # Convert queryset to Dataframe
    #q = all_objects.values('program_select', 'hours_spent', 'minutes_spent')
    #q = all_objects.values()
    #df = pd.DataFrame.from_records(q) # Convert queryset to dataframe

    #mydf = df.to_json()
    #test_data_as_json = serializers.serialize("json", df, use_natural_keys=True)
    #request.session['table_display'] = "Hello World"

    return render(request, "report.html", {
                  #'test_data_as_json': test_data_as_json,
                  'df': table_display.to_html(),
                  'date_form': date_form
                  })
