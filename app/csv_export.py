"""
This script asks as a module that writes a data model to a CSV for download.
There is a dummy csv for initial app testing and a state time series CSV.
"""

import app.models as mdl

import csv
from io import StringIO

#this was a dummy csv I used for the initial demo page
def generate_dummy_csv():

    x = list(range(0, 100))
    y = list(range(0, 200, 2))

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['X', 'Y'])

    for i, j in zip(x, y):
        writer.writerow([i, j])

    output.seek(0)

    return output.getvalue()

# this function serves a CSV that combines the data for each of the time series visualizations
def mortgage_averages(state_name):

    df1 = mdl.StateLoanAmount(state_name= state_name).return_df()
    df2 = mdl.StateInterestRateSeries(state_name= state_name).return_df()
    df3 = mdl.StateLTV(state_name= state_name).return_df()
    df4 = mdl.StateLoanVolumes(state_name= state_name).return_df()

    df1 = df1.rename(columns= {'value': 'Total Loan Amount'})
    df2 = df2.rename(columns= {'value': 'Average Interest Rate'})
    df3 = df3.rename(columns= {'value': 'Average LTV'})
    df4 = df4.rename(columns= {'value': 'Loan Volume'})

    join1 = df1.merge(df2, how = 'inner', on = ['Year','State','Loan Term'])
    join2 = join1.merge(df3, how = 'inner', on = ['Year','State','Loan Term'])

    final_join = join2.merge(df4, how = 'inner', on = ['Year','State','Loan Term'])

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Year', 'State', 'Loan Term', 'Total Loan Amount', 'Average Interest Rate', 'Average LTV', 'Loan Volume'])

    for index, row in final_join.iterrows():
        writer.writerow([row['Year'], row['State'], row['Loan Term'], row['Total Loan Amount'], row['Average Interest Rate'], row['Average LTV'], row['Loan Volume']])

    output.seek(0)

    return output.getvalue()
