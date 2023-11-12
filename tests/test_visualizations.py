import unittest
from flask import current_app
from app import create_app
from app import visualizations as vis
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

class TestVisualizations(unittest.TestCase):

    def interest_rates_test(self, state_name):
        try:
            plot = vis.state_interest_rates(state_name=state_name)
            bin_data = base64.b64decode(plot)

            with open(f'tests/interest_rate_graphs/{state_name}_interest_rate.png', 'wb') as f:
                f.write(bin_data)
        except Exception as e:
            print(e)

    def test_visualizations(self):
        state_list = ['AZ', 'CO', 'NM', 'UT']

        for state in state_list:
            self.interest_rates_test(state_name=state)