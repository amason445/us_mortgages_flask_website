from app.config import Config
import app.utilities as utl

from abc import ABC, abstractmethod

import requests
import pandas as pd

# I wrote a simple interace for the CouchDB querying to help with unit testing
# I used an abstract method and based it off the below in Java
# https://www.w3schools.com/java/java_interface.asp

class CouchDBQuery(ABC):
  
    def __init__(self, state_name):
        self.state_name = state_name

    @abstractmethod
    def return_df(self):
        pass

class StateLoanVolumes(CouchDBQuery):

    request_url = Config.COUCHDB_ROOT_URL +  '//state_mortgage_records_v2//_design//state_mortgages_design_//_view//year_state_records?group=true'

    def return_df(self):
        request = requests.get(self.request_url)
        request_data = request.json()
        df = pd.DataFrame(request_data['rows'])
        df[['Year', 'State']] = pd.DataFrame(df['key'].to_list(), index= df.index)
        df = df[['Year','State', 'value']]
        df = df[df['State'] == self.state_name]

        return df


class StateInterestRateSeries(CouchDBQuery):

    request_url = Config.COUCHDB_ROOT_URL + 'state_mortgage_records_v2//_design//state_mortgages_design_//_view//average_interest_rate_per_state?group=true'

    def return_df(self):
           
        request = requests.get(self.request_url)
        request_data = request.json()
        df = pd.DataFrame(request_data['rows'])
        df[['Year', 'State', 'Loan Term']] = pd.DataFrame(df['key'].to_list(), index= df.index)
        df = df[['Year','State', 'Loan Term', 'value']]
        df = df[df['State'] == self.state_name]
        df['Loan Term'] = (df['Loan Term'] // 12).astype(str) + '-year'
        df['value'] = df['value'].round(2)
        
        return df
    
class StateLoanAmount(CouchDBQuery):
    pass

    # request_url = Config.COUCHDB_ROOT_URL +  '//state_mortgage_records_v2//_design//state_mortgages_design_//_view//year_state_records?group=true'

    # def return_df(self):
    #     request = requests.get(self.request_url)
    #     request_data = request.json()
    #     df = pd.DataFrame(request_data['rows'])
    #     df[['Year', 'State']] = pd.DataFrame(df['key'].to_list(), index= df.index)
    #     df = df[['Year','State', 'value']]
    #     df = df[df['State'] == self.state_name]

    #     return df

