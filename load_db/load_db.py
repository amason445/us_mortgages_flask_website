import logging
logging.basicConfig(filename='logging\\db_load.log', encoding='utf-8', level=logging.INFO, 
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import itertools

import multiprocessing
import worker
from functools import partial

if __name__ == '__main__':

    years = [2022, 2021, 2020, 2019, 2018]

    state_abbreviations = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
                'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
                'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
                'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
    
    state_years = list(itertools.product(years, state_abbreviations))

    try:
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    
        pool.map(func= partial(worker.worker), iterable= state_years)

        pool.close()
        pool.join()

    except Exception as e:
        logging.error(f'Error:\n {e}')
        pass
 

