from datetime import datetime
from tabulate import tabulate

green = '\u001b[32m'
blue = '\033[94m'
red = '\033[91m'
end_character = '\033[0m'

# Print timestamped log messages, coloured based on message type

def info(message):
    
    print(green + "[" + get_now() + "] " + message + end_character)

def error(message):
    
    print(red + "[" + get_now() + "] " + message + end_character)

def dataframe(df, show_index=False):
    
    print(red + "[" + get_now() + "]\n" + tabulate(df, headers='keys', tablefmt='psql', showindex=show_index) + end_character)

def get_now():
    
    return datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
