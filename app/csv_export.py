from flask import make_response

import app.models as mdl

import csv
from io import StringIO
import pandas as pd

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

def mortgage_volume(state_name):

    df = mdl.StateLoanVolumes(state_name= state_name).return_df()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Year', 'State', 'Number of Loans'])

    for index, row in df.iterrows():
        writer.writerow([row['Year'], row['State'], row['value']])

    output.seek(0)

    return output.getvalue()

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
    writer.writerow(['Year', 'State', 'Loan Amount', 'Average Interest Rate', 'Average LTV', 'Loan Volume'])

    for index, row in final_join.iterrows():
        writer.writerow([row['Year'], row['State'], row['Loan Amount'], row['Average Interest Rate'], row['Average LTV'], row['Loan Volume']])

    output.seek(0)

    return output.getvalue()
