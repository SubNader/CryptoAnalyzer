import pandas as pd
from pathlib import Path
from urllib.parse import urlencode
from datetime import datetime as dt


def fetch_data(configurations, save=False):
    
    # API URL and parameters
    api_url = configurations['api']['url']
    params = {
        'function': configurations['api']['function'],
        'apikey': configurations['api']['key'],
        'symbol': configurations['api']['currency'],
        'market': configurations['api']['market'],
        'datatype': configurations['api']['format']
    }
    
    # Encode URL parameters
    encoded_parameters = urlencode(params)
    
    # Create full data URL
    data_url = f"{api_url}?{encoded_parameters}"

    # Pull data from the API into a dataframe
    data = pd.read_csv(data_url)
    
    # Save data if required
    if save:
        
        # Create save path
        save_format = configurations['storage']['format']
        save_directory = configurations['storage']['directory']
        timestamp = dt.now().strftime("%Y%m%d%H%M")
        save_path = f"{save_directory}/{params.get('symbol')}_{params.get('market')}_{timestamp}.{save_format}"

        # Ensure save directory is present
        Path(save_directory).mkdir(exist_ok=True)
        
        # Save data to disk based on configured format
        if save_format == 'json':
            data.to_json(save_path, index=None)
        else:
            data.to_csv(save_path, index=None)
        
    return data