import pandas as pd
from . import logger
from pathlib import Path
from copy import deepcopy
from datetime import datetime as dt


def analysis_save_attributes(configurations, mode, verify_directory=False):

    timestamp = dt.now().strftime("%Y%m%d")
    currency = configurations['api']['currency']
    market = configurations['api']['market']
    save_format = configurations['analysis_data']['format']
    save_directory = configurations['analysis_data']['directory']
    save_path = f"{save_directory}/{currency}_{market}_{mode}_{timestamp}.{save_format}"

    # Ensure save directory is present, if required
    if verify_directory:
        Path(save_directory).mkdir(parents=True, exist_ok=True)
    
    return save_path, save_format


def weekly_mean_prices(fetched_data, configurations, save=False):
    
    # Report starting 
    logger.info("Computing weekly mean prices..")
    
    # Create a local copy of data
    data = deepcopy(fetched_data)
    
    # Make the data timestamp-indexed
    data.reset_index(inplace=True)
    data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
    data.set_index('timestamp', inplace=True)
        
    # Get market symbol - needed for column name
    market = configurations['api']['market']
    
    # Compute weekly means
    data['weekly_mean'] = data[f'close ({market})'].resample('W-MON').mean()
    
    # Clean up final dataframe
    data.rename_axis('week_start', inplace=True)
    data.reset_index(drop=False, inplace=True)
    weekly_means = data[data.weekly_mean.notnull()][['week_start','weekly_mean']]
    
    # Free memory up
    del data
    
    if save:
        
        # Get output attributes
        save_path, save_format = analysis_save_attributes(configurations, mode='weekly_means', verify_directory=True)

        # Save data to disk based on configured format
        try:
            if save_format == 'json':
                weekly_means.to_json(save_path, orient='table', index=False)
            else:
                weekly_means.to_csv(save_path, index=None)
        except:
            logger.error("Failed to save weekly means {} data to {}. Terminating..".format(save_format.upper(), save_path))
            exit(1)
        else:
            logger.info("Saved weekly means {} data to {}".format(save_format.upper(), save_path))
            
            
    return weekly_means


def maximum_relative_spans(fetched_data, configurations, n_highest_weeks=1):

    # Report starting 
    logger.info("Finding the first {} week(s) with highest relative span values..".format(n_highest_weeks))
    
    # Create a local copy of data
    data = deepcopy(fetched_data)
    
    # Make the data timestamp-indexed
    data.reset_index(inplace=True)
    data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
    data.set_index('timestamp', inplace=True)
    
    # Resample data to weekly
    weekly_data = data.resample('W-MON')
    
    # Get market symbol - needed for column name
    market = configurations['api']['market']

    # Compute min and max closing price per week
    data['min_closing_price'] = weekly_data[f'close ({market})'].min()
    data['max_closing_price'] = weekly_data[f'close ({market})'].max()
    
    # Compute weekly relative spans
    data['relative_span'] = data.apply(lambda row: (row['max_closing_price'] - row['min_closing_price'])/row['min_closing_price'], axis=1)

    # Clean up final dataframe
    data.rename_axis('week_start', inplace=True)
    data.reset_index(drop=False, inplace=True)
    
    # Get N weeks of maximum relative spans 
    maximum_weekly_relative_spans = data.sort_values('relative_span', ascending=False)
    max_n_relative_spans = maximum_weekly_relative_spans[['week_start', 'relative_span']].head(n_highest_weeks)
    
    # Report value
    logger.info("The week(s) with highest relative span values are as follows, in descending order:")
    logger.dataframe(max_n_relative_spans)
    
    