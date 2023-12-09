"""
This script is a module containing several utility functions.
"""

import requests
import pandas as pd

# converts the state abbreviations to the full state names
def state_abbreviation_mapping(abbreviation):
    match abbreviation:
        case 'AZ':
            return 'Arizona'
        case 'CO':
            return 'Colorado'
        case 'NM':
            return 'New Mexico'
        case 'UT':
            return 'Utah'
        
# maps the state names to the coordinates of their capital cities
# googled them and took them from here: https://www.latlong.net/
def state_capital_coordinates(abbreviation):
        match abbreviation:
            case 'AZ':
                return [33.4484, -112.0740]
            case 'CO':
                return [39.7392,-104.991531]
            case 'NM':
                return [35.691544, -105.944183]
            case 'UT':
                return [40.758701, -111.876183]


# this function is used in the data models to standardize requests from CouchDB and load them to dataframes
def request_to_df(url_string):
        request = requests.get(url_string)
        request_data = request.json()
        return pd.DataFrame(request_data['rows'])