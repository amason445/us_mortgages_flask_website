from app.config import Config
import app.utilities as utl
import requests
import pandas as pd
from matplotlib import pyplot as plt
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

def state_interest_rates(state_name):
    try:

        request_url = Config.COUCHDB_ROOT_URL + 'state_mortgage_records_v2//_design//state_mortgages_design_//_view//average_interest_rate_per_state?group=true'

        request = requests.get(request_url)

        request_data = request.json()

        df = pd.DataFrame(request_data['rows'])

        df[['Year', 'State']] = pd.DataFrame(df['key'].to_list(), index= df.index)

        df = df[['Year','State','value']]

        df = df[df['State'] == state_name]

        df['value'] = df['value'].round(2)

        x = df['Year'].astype(int)
        y = df['value']

        plt.plot(x,y)

        plt.locator_params(axis="x", integer=True, tight=True)
        
        plt.title(f"Average Interest Rates for the US State of {utl.state_abbreviation_mapping(state_name)}")
        plt.xlabel('Year')
        plt.ylabel('Interest Rate')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        plt.clf()
        
        return base64.b64encode(buffer.read()).decode()
    
    except Exception as e:
        print(e)
