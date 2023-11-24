from app.config import Config
import app.utilities as utl

from abc import ABC, abstractmethod

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
        df = utl.request_to_df(self.request_url)
        df[['Year', 'State']] = pd.DataFrame(df['key'].to_list(), index= df.index)
        df = df[['Year','State', 'value']]
        df = df[df['State'] == self.state_name]

        return df


class StateInterestRateSeries(CouchDBQuery):

    request_url = Config.COUCHDB_ROOT_URL + 'state_mortgage_records_v2//_design//state_mortgages_design_//_view//average_interest_rate_per_state?group=true'

    def return_df(self):
        df = utl.request_to_df(self.request_url)
        df[['Year', 'State', 'Loan Term']] = pd.DataFrame(df['key'].to_list(), index= df.index)
        df = df[['Year','State', 'Loan Term', 'value']]
        df = df[df['State'] == self.state_name]
        df['Loan Term'] = (df['Loan Term'] // 12).astype(str) + '-year'
        df['value'] = df['value'].round(2)
        
        return df
    
class StateLoanAmount(CouchDBQuery):
    pass

    request_url = Config.COUCHDB_ROOT_URL +  '//state_mortgage_records_v2//_design/state_mortgages_design_//_view//total_loaned_per_state?group=true'

    def return_df(self):
        df = utl.request_to_df(self.request_url)
        df[['Year', 'State', 'Loan Term']] = pd.DataFrame(df['key'].to_list(), index= df.index)
        df = df[['Year','State', 'Loan Term', 'value']]
        df = df[df['State'] == self.state_name]
        df['Loan Term'] = (df['Loan Term'] // 12).astype(str) + '-year'
        df['value'] = df['value'].round(2)
        
        return df

class StateLTV(CouchDBQuery):

    request_url = Config.COUCHDB_ROOT_URL +  '//state_mortgage_records_v2//_design//state_mortgages_design_//_view//average_ltv_per_state?group=true'

    def return_df(self):
        df = utl.request_to_df(self.request_url)
        df[['Year', 'State', 'Loan Term']] = pd.DataFrame(df['key'].to_list(), index= df.index)
        df = df[['Year','State', 'Loan Term', 'value']]
        df = df[df['State'] == self.state_name]
        df['Loan Term'] = (df['Loan Term'] // 12).astype(str) + '-year'
        df['value'] = df['value'].round(2)

        return df

class CountyGeo(CouchDBQuery):
    county_total_volume_amount_url = Config.COUCHDB_ROOT_URL +  '//state_mortgage_records_v2//_design/state_mortgages_design_//_view//total_loans_by_county?group=true'
    county_interest_rate_url = Config.COUCHDB_ROOT_URL + 'state_mortgage_records_v2//_design//state_mortgages_design_//_view//average_interest_rate_per_county?group=true'
    county_loan_amount_url = Config.COUCHDB_ROOT_URL +  '//state_mortgage_records_v2//_design/state_mortgages_design_//_view//total_loaned_by_county?group=true'
    county_ltv_url = Config.COUCHDB_ROOT_URL +  '//state_mortgage_records_v2//_design//state_mortgages_design_//_view//average_ltv_per_county?group=true'

    def return_df(self):
        volume_df = utl.request_to_df(self.county_total_volume_amount_url)
        interest_df = utl.request_to_df(self.county_interest_rate_url)
        loan_amount_df = utl.request_to_df(self.county_loan_amount_url)
        ltv_df = utl.request_to_df(self.county_ltv_url)

        volume_df[['Year', 'State', 'County', 'Loan Term']] = pd.DataFrame(volume_df['key'].to_list(), index= volume_df.index)
        interest_df[['Year', 'State', 'County', 'Loan Term']] = pd.DataFrame(interest_df['key'].to_list(), index= interest_df.index)
        loan_amount_df[['Year', 'State', 'County', 'Loan Term']] = pd.DataFrame(loan_amount_df['key'].to_list(), index= loan_amount_df.index)
        ltv_df[['Year', 'State', 'County', 'Loan Term']] = pd.DataFrame(ltv_df['key'].to_list(), index= ltv_df.index)

        volume_df = volume_df[['Year','State', 'County', 'Loan Term', 'value']]
        interest_df = interest_df[['Year','State', 'County', 'Loan Term', 'value']]
        loan_amount_df = loan_amount_df[['Year','State', 'County', 'Loan Term', 'value']]
        ltv_df = ltv_df[['Year','State', 'County', 'Loan Term', 'value']]

        volume_df = volume_df.rename(columns= {'value': 'Loan Volume'})
        interest_df = interest_df.rename(columns= {'value': 'Average Interest Rate'})
        loan_amount_df = loan_amount_df.rename(columns= {'value': 'Total Loan Amount'})
        ltv_df = ltv_df.rename(columns= {'value': 'Average Loan to Value'})

        join_df_1 = volume_df.merge(interest_df, how = 'inner', on = ['Year', 'State', 'County', 'Loan Term'])
        join_df_2 = join_df_1.merge(loan_amount_df, how = 'inner', on = ['Year', 'State', 'County', 'Loan Term'])
        final_df = join_df_2.merge(ltv_df, how = 'inner', on = ['Year', 'State', 'County', 'Loan Term'])

        final_df = final_df[final_df['State'] == self.state_name]
        final_df['Loan Term'] = (final_df['Loan Term'] // 12).astype(str) + '-year'

        return final_df


