import requests

from bs4 import BeautifulSoup

import socket

import datetime

from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

import smtplib

import os

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

# Check for relevant roles on the webpage
def check_relevant_roles():
    site_url = 'https://langara.wd10.myworkdayjobs.com/External_Employment_Opportunities'

    # Start WebDriver and load page
    log('Loading page...')
    wd = webdriver.Chrome()
    wd.get(site_url)

    # Wait for dynamically loaded elements
    WebDriverWait(wd, 10).until(EC.visibility_of_element_located((By.ID, "wd-FacetedSearchResultList-facetSearchResultList.newFacetSearch.Report_Entry")))

    # Fetch and parse HTML content
    log('Fetching and parsing HTML...')
    html_page = wd.page_source
    wd.quit()
    soup = BeautifulSoup(html_page, 'lxml')

    # Get relevant jobs
    log('Looking for relevant jobs...')
    job_soup = soup.find('div', {'id': 'wd-FacetedSearchResultList-facetSearchResultList.newFacetSearch.Report_Entry'})

    roles_soup = job_soup.find_all('div', class_='gwt-Label')

    roles = []
    for role in roles_soup:
        if(('WOC' in role.get_text() and '2021' in role.get_text()) or ('SWAP' in role.get_text() and '2021' in role.get_text())):
            roles.append(role.get_text())

    return(roles)

# Send mail
def send_mail(relevant_roles, status):

    # Current date and time
    dt = datetime.datetime.now()
    dt_format = dt.strftime('%B %d, %Y (%A) at %H:%M')

    # Get username and password
    user = os.environ.get('EMAIL_USER')
    pwd = os.environ.get('EMAIL_PASS')

    # Set up connection
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Login
    server.login(user, pwd)

    subject = 'Langara WAC/SWAP Applications Open'

    # Check status and prepare body
    if(status == 'success'):

        log('Preparing body for success mail...')

        body = f'The following job openings were found on {dt_format}:'
        body += '\n----------------------------------------------------------------------------------------------------------------------------------------'
        for index, role in enumerate(relevant_roles):
            body += f'\n{index + 1}. {role}'
        body += '\n----------------------------------------------------------------------------------------------------------------------------------------'

    # Error message
    else:

        log('Preparing mail body for error mail...')

        body = f'Error: {status}.\nCheck your code.'

    # Prepare mail
    message = f'Subject: {subject}\n\n{body}'
    message = message.encode('utf-8')

    # Send mail
    server.sendmail(user, user, message)

    log('Mail sent!')

    # End connection
    server.quit()
