import logging
logging.basicConfig(filename='logging\\games.log', encoding='utf-8', level=logging.INFO, 
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import requests
import csv
import json
from io import StringIO


years = [2018,2019,2020,2021,2022]
state_acronyms = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

for year in years:
    for state in state_acronyms:

        hmda_api_request = f'https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?states={state}&years={year}'

        try:
            response = requests.request(hmda_api_request)
            request_csv = response.text

            results_list = []

            csv_reader = csv.DictReader(StringIO(request_csv))

            for row in csv_reader:
                results_list.append(json.dumps(row))

        except Exception as e:
            logging.error(f'Errror when accesing API:\n {e}')


