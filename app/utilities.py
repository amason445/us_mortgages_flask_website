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

def request_to_df(url_string):
        request = requests.get(url_string)
        request_data = request.json()
        return pd.DataFrame(request_data['rows'])