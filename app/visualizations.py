"""
This script acts a module that renders visualizations for the time series pages. 
Each function acceses a model and then renders a plot using seaborn or matplotlib.
The plots have to be returned as byte strings to be rendered.
"""

import app.utilities as utl
import app.models as mdl


# matplotlib doesn't like multithreading. I had to swap the backend to allow it to work with flask.
import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt

import seaborn as sns
from io import BytesIO
import base64

def dummy_plot():
    
    x = range(0, 100)
    y = range(0, 200, 2)

    plt.plot(x, y)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return base64.b64encode(buffer.read()).decode()

def state_loan_volumes(state_name):
    try:

        df = mdl.StateLoanVolumes(state_name= state_name).return_df()

        sns.barplot(data = df, x = 'Year', y = 'value', hue= 'Loan Term')

        ax = plt.gca()
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

        plt.title(f"Loan Volume for the US State of {utl.state_abbreviation_mapping(state_name)}")
        plt.xlabel('Year')
        plt.ylabel('Loan Volume')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        plt.clf()
        plt.close()
        
        return base64.b64encode(buffer.read()).decode()
    
    except Exception as e:
        print(e)


def state_interest_rates(state_name):
    try:

        df = mdl.StateInterestRateSeries(state_name= state_name).return_df()

        sns.lineplot(data = df, x = 'Year', y = 'value', hue= 'Loan Term')
        
        ax = plt.gca()
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        
        plt.title(f"Average Interest Rates for the US State of {utl.state_abbreviation_mapping(state_name)}")
        plt.xlabel('Year')
        plt.ylabel('Interest Rate (%)')
        plt.legend(title = 'Loan Term')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        plt.clf()
        plt.close()
        
        return base64.b64encode(buffer.read()).decode()
    
    except Exception as e:
        print(e)

def state_ltvs(state_name):
    try:

        df = mdl.StateLTV(state_name=state_name).return_df()

        sns.lineplot(data = df, x = 'Year', y = 'value', hue= 'Loan Term')
        
        ax = plt.gca()
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        
        plt.title(f"Average Loan to Value for the US State of {utl.state_abbreviation_mapping(state_name)}")
        plt.xlabel('Year')
        plt.ylabel('Loan to Value (%)')
        plt.legend(title = 'Loan Term')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        plt.clf()
        plt.close()
        
        return base64.b64encode(buffer.read()).decode()
    
    except Exception as e:
        print(e)

def state_loan_amounts(state_name):
    try:

        df = mdl.StateLoanAmount(state_name=state_name).return_df()

        df['value'] = df['value'] / 1000000

        sns.lineplot(data = df, x = 'Year', y = 'value', hue= 'Loan Term')
        
        ax = plt.gca()
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        
        plt.title(f"Loan Volume ($) for the US State of {utl.state_abbreviation_mapping(state_name)}")
        plt.xlabel('Year')
        plt.ylabel('Loan Volume ($0000)')
        plt.legend(title = 'Loan Term')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        plt.clf()
        plt.close()
        
        return base64.b64encode(buffer.read()).decode()
    
    except Exception as e:
        print(e)