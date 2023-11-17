import unittest
from flask import current_app
from app import create_app
from app import models as mdl
from app import visualizations as vis

import pandas as pd
import base64

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

class TestModels(unittest.TestCase):
    def loan_volume_model_test(self, state_name):
        try:
            df = mdl.StateLoanVolumes(state_name= state_name).return_df()

            if df is not None:
                df.to_csv(f'tests/models/loan_volume_models/{state_name}_volumes.csv', index= False)
            else:
                print(f"Failed to fetch data for state {state_name}")

        except Exception as e:
            print(e)

    def interest_rate_model_test(self, state_name):
        try:
            df = mdl.StateInterestRateSeries(state_name= state_name).return_df()

            if df is not None:
                df.to_csv(f'tests/models/interest_rate_models/{state_name}_interest_rate.csv', index= False)
            else:
                print(f"Failed to fetch data for state {state_name}")

        except Exception as e:
            print(e)

    def loan_to_value_model_test(self, state_name):
        try:
            df = mdl.StateLTV(state_name= state_name).return_df()

            if df is not None:
                df.to_csv(f'tests/models/ltv_models/{state_name}_ltv.csv', index= False)
            else:
                print(f"Failed to fetch data for state {state_name}")

        except Exception as e:
            print(e)


    def test_models(self):
        state_list = ['AZ', 'CO', 'NM', 'UT']

        for state in state_list:
            self.loan_volume_model_test(state_name=state)
            self.interest_rate_model_test(state_name= state)
            self.loan_to_value_model_test(state_name= state)

class TestVisualizations(unittest.TestCase):

    def loan_volumes_test(self, state_name):
        try:
            plot = vis.state_loan_volumes(state_name=state_name)
            bin_data = base64.b64decode(plot)

            with open(f'tests/graphs/loan_volume_graphs/{state_name}_volumes.png', 'wb') as f:
                f.write(bin_data)
                f.close()

        except Exception as e:
            print(e)


    def interest_rates_test(self, state_name):
        try:
            plot = vis.state_interest_rates(state_name=state_name)
            bin_data = base64.b64decode(plot)

            with open(f'tests/graphs/interest_rate_graphs/{state_name}_interest_rate.png', 'wb') as f:
                f.write(bin_data)
                f.close()

        except Exception as e:
            print(e)

    def ltvs_test(self, state_name):
        try:
            plot = vis.state_ltvs(state_name=state_name)
            bin_data = base64.b64decode(plot)

            with open(f'tests/graphs/ltv_graphs/{state_name}_ltv_graphs.png', 'wb') as f:
                f.write(bin_data)
                f.close()

        except Exception as e:
            print(e)


    def test_visualizations(self):
        state_list = ['AZ', 'CO', 'NM', 'UT']

        for state in state_list:
            self.loan_volumes_test(state_name=state)
            self.interest_rates_test(state_name=state)
            self.ltvs_test(state_name=state)
