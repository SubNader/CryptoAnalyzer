import pandas as pd
from . import logger
from pathlib import Path
from urllib.parse import urlencode
from datetime import datetime as dt


def raw_save_attributes(configurations, verify_directory=False):

    timestamp = dt.now().strftime("%Y%m%d")
    currency = configurations['api']['currency']
    market = configurations['api']['market']
    save_format = configurations['raw_data']['format']
    save_directory = configurations['raw_data']['directory']
    save_path = f"{save_directory}/{currency}_{market}_{timestamp}.{save_format}"

    # Ensure save directory is present, if required
    if verify_directory:
        Path(save_directory).mkdir(parents=True, exist_ok=True)

    return save_path, save_format


def fetch_data(configurations, save=False):
    
    # Report starting
    logger.info("Loading data from API..")
    
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
    data = None
    try:
        data = pd.read_csv(data_url)
    except:
        logger.error("Failed to load data. Terminating..")
        exit(1)
    else:
        logger.info("Loaded data successfully.")

    # Save data if required
    if save:

        # Get output attributes
        save_path, save_format = raw_save_attributes(configurations, verify_directory=True)

        # Save data to disk based on configured format
        try:
            if save_format == 'json':
                data.to_json(save_path, orient='table', index=False)
            else:
                data.to_csv(save_path, index=None)
        except:
            logger.error("Failed to save raw {} data to {}. Terminating..".format(save_format.upper(), save_path))
            exit(1)
        else:
            logger.info("Saved raw {} data to {}".format(save_format.upper(), save_path))


    return data