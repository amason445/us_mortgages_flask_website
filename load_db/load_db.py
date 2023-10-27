import logging
logging.basicConfig(filename='logging\\db_load.log', encoding='utf-8', level=logging.INFO, 
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import itertools

import multiprocessing
import worker
from functools import partial

if __name__ == '__main__':

    years = [2022, 2021, 2020, 2019, 2018]

    state_abbreviations = ['CO', 'UT', 'AZ', 'NM']
    
    state_years = list(itertools.product(years, state_abbreviations))

    try:

        cpu_floor = multiprocessing.cpu_count() - 2

        pool = multiprocessing.Pool(processes= cpu_floor)
    
        pool.map(func= partial(worker.worker), iterable= state_years)

        pool.close()
        pool.join()

    except Exception as e:
        logging.error(f'Error:\n {e}')
        pass
 

