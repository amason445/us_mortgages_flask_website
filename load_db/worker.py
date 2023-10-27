import logging

import toml

import couchdb
import requests
import csv
from io import StringIO

def worker(data_tuple):

    load_config = toml.load('load_db/config_load.toml')

    couch = couchdb.Server(load_config['CouchDB']['connection_string'])

    couch_db = couch[load_config['CouchDB']['loan_records_db']]

    logging.info(f'Worker initialized for: {data_tuple[0]}-{data_tuple[1]}')

    hmda_api_request = f'https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?states={data_tuple[1]}&years={data_tuple[0]}&actions_taken=1'

    #logging.info(f'{hmda_api_request}')

    try:
        response = requests.request('GET', hmda_api_request)
        request_csv = response.text

        logging.info(f'{data_tuple[0]}-{data_tuple[1]} API pull: {response.status_code}')

        results_list = []

        csv_reader = csv.DictReader(StringIO(request_csv))

        for row in csv_reader:
            results_list.append(row)

        logging.info(f'{data_tuple[0]}-{data_tuple[1]} JSON conversion was successful. Records size: {len(results_list)}')

        chunk_size = 1000
        record_chunks = [results_list[i: i + chunk_size] for i in range(0, len(results_list), chunk_size)]

        counter = 0

        for i in range(0,len(record_chunks)):       
            
            load_fragment = {}

            load_fragment['_id'] = f'{data_tuple[0]}-{data_tuple[1]}-{i}'
            load_fragment['year'] = data_tuple[0]
            load_fragment['state'] = data_tuple[1]
            load_fragment['record_chunk'] = record_chunks[i]

            couch_db.save(load_fragment)

            counter += 1

        logging.info(f'{data_tuple[0]}-{data_tuple[1]}. JSON load to DB was successful. Number of Record Chunks: {counter}')

    except Exception as e:
        logging.error(f'Error when accessing API:\n {e}')
        pass