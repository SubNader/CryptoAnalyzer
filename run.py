from lib import analyze, config, client, logger


def run():

    # Report starting
    logger.info("Starting CryptoAnalyzer..")
    
    # Load configurations
    configurations = config.load()
    
    # Fetch data and save it to disk
    fetched_data = client.fetch_data(configurations, save=True)
    
    # Compute weekly means
    analyze.weekly_mean_prices(fetched_data, configurations, save=True)
    
    # Compute maximum relative span
    analyze.maximum_relative_spans(fetched_data, configurations, n_highest_weeks=1)
    
    # Report completion
    logger.info("Done. Exiting..")
    
    # Exit
    exit(0)
    
if __name__ == '__main__':
    run()