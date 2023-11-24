import requests
import pandas as pd

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
        
def request_to_df(url_string):
        request = requests.get(url_string)
        request_data = request.json()
        return pd.DataFrame(request_data['rows'])