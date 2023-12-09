"""
This script contains the load function and scoping. It accesses the Consumer Protection Finance Bureau API below and scrapes CSVs by state and year.
Since the data was rather larged, I used Python's multiprocessing library. So, this folder includes a worker function that process each individual CSV.
The CSVs are converted into dictionaries and then loaded into CouchDB as JSON. Database pathing is set in a toml file called Config.toml.
I included a template file for this toml for my privacy. It's copied from the file I set in my .gitignore but removes sensitive information.
The process does not guarantee consistency and it is possible for individual documents to fail. Therefore, it's important to check logs and reupload if necessary.
https://ffiec.cfpb.gov/documentation/api/data-browser/
"""


import logging
logging.basicConfig(filename='load_db\\logging\\db_load.log', encoding='utf-8', level=logging.INFO, 
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import itertools

import multiprocessing
import worker
from functools import partial

if __name__ == '__main__':

    # these lists contain the data base scope
    years = [2022, 2021, 2020, 2019, 2018]
    state_abbreviations = ['CO', 'UT', 'AZ', 'NM']
    
    # the year and state lists are packaged into tuples using a cartesian product
    state_years = list(itertools.product(years, state_abbreviations))

    try:

        #sets the maximum number of CPUs for the multiprocessing. I subtracted two to conserve CPU resources during the load
        cpu_floor = multiprocessing.cpu_count() - 2

        #this builds a CPU pool for the workers defined in the worker function
        pool = multiprocessing.Pool(processes= cpu_floor)
    
        #this maps the workers to the CPU pool and iterates over the tuples defines by the scoping
        pool.map(func= partial(worker.worker), iterable= state_years)

        pool.close()
        pool.join()

    except Exception as e:
        logging.error(f'Error:\n {e}')
        pass
 

