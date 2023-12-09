"""
This script is a module whihc contains the data models from CouchDB. 
These models are implemeneted similarly to an interface in Java like below.
There is an abstract class called CouchDBQuery that each model inherits from.
Currently, a CouchDB design document is queries and returned as a Pandas Dataframe.
Sometimes, multiple design documents are joined together like in the county geo model.
https://www.w3schools.com/java/java_interface.asp
"""


from app.config import Config
import app.utilities as utl

from abc import ABC, abstractmethod

import pandas as pd

# abstract class that defines the interface 
class CouchDBQuery(ABC):
  
    def __init__(self, state_name):
        self.state_name = state_name

    @abstractmethod
    def return_df(self):
        pass

# this class defines the state mortgage loan volumes
class StateLoanVolumes(CouchDBQuery):

    request_url = Config.COUCHDB_ROOT_URL +  '//state_mortgage_records_v2//_design//state_mortgages_design_//_view//total_loan_volume_per_state?group=true'

    def return_df(self):
        df = utl.request_to_df(self.request_url)
        df[['Year', 'State', 'Loan Term']] = pd.DataFrame(df['key'].to_list(), index= df.index)
        df = df[['Year','State','Loan Term', 'value']]
        df = df[df['State'] == self.state_name]
        df['Loan Term'] = (df['Loan Term'] // 12).astype(str) + '-year'

        return df


# this class defines the state interest rates
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
    
# this class defines the state mortgage loan amounts
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

# this class defines the state mortgage loan to values
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

# this class defines the state county geo data
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

        final_df = final_df.drop(final_df[final_df['County'] == 'NA'].index)
        final_df['County'] = final_df['County'].astype(str)

        return final_df


