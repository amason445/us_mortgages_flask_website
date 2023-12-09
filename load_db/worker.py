"""
This script contains the worker function for the load process. The worker function creates a worker and assigns it to the CPU pool.
The function accesses the API below and pulls a CSV based on year and state. It then converts the CSV into a JSON document and loads it to CouchDB.
Each JSON document contains 1000 records from each CSV. They are loaded into CouchDB as record chunks.
https://ffiec.cfpb.gov/documentation/api/data-browser/
"""



import logging

import toml

import couchdb
import requests
import csv
from io import StringIO

def worker(data_tuple):

    # contains pathing information for the CouchDB database
    load_config = toml.load('load_db/config_load.toml')

    # initializes CouchDB connection
    couch = couchdb.Server(load_config['CouchDB']['connection_string'])
    couch_db = couch[load_config['CouchDB']['loan_records_db']]

    logging.info(f'Worker initialized for: {data_tuple[0]}-{data_tuple[1]}')

    # this is the API request URL. It uses the tuple as parameters.
    hmda_api_request = f'https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?states={data_tuple[1]}&years={data_tuple[0]}&actions_taken=1'

    #logging.info(f'{hmda_api_request}')

    try:
        
        # GET request against the CFPB API
        response = requests.request('GET', hmda_api_request)
        request_csv = response.text
        logging.info(f'{data_tuple[0]}-{data_tuple[1]} API pull: {response.status_code}')

        # reads results to CSV and converts records to a records dictionary
        results_list = []
        csv_reader = csv.DictReader(StringIO(request_csv))

        for row in csv_reader:
            results_list.append(row)

        logging.info(f'{data_tuple[0]}-{data_tuple[1]} JSON conversion was successful. Records size: {len(results_list)}')

        # slices records dictionaries into a list of lists where each list will contain 1000 chunks
        chunk_size = 1000
        record_chunks = [results_list[i: i + chunk_size] for i in range(0, len(results_list), chunk_size)]

        counter = 0

        # each chunk is uploaded structured into an individual JSON document and uploaded to CouchDB
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