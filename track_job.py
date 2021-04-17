import requests

from bs4 import BeautifulSoup

import socket

import datetime

# Log outcome to text file every time the program is run


def log(message):
    # Current date and time
    dt = datetime.datetime.now()
    dt_format = dt.strftime('%B %d, %Y (%H:%M:%S):')

    # Write to file
    with open('log.txt', 'a', encoding='utf-8') as f_out:
        f_out.write(f'{dt_format} {message}\n')

# Check if an internet connection is present


def is_connected():
    # Write to log file
    with open('log.txt', 'a', encoding='utf-8') as f_out:
        f_out.write('\n')

    log('Checking connection...')

    try:
        # Connect to the host (tells if the host is actually reachable)
        socket.create_connection(("1.1.1.1", 53))
        return True

    except OSError:
        pass

    return False


if(is_connected()):
    log('Internet connection available.')

else:
    log('No internet connection.')
