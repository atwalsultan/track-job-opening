import requests

from bs4 import BeautifulSoup

import socket

import datetime

from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

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


def check_relevant_roles():
    site_url = 'https://langara.wd10.myworkdayjobs.com/External_Employment_Opportunities'

    # Start WebDriver and load page
    log('Loading page...')
    wd = webdriver.Chrome()
    wd.get(site_url)

    # Wait for dynamically loaded elements
    WebDriverWait(wd, 10).until(EC.visibility_of_element_located(
        (By.ID, "wd-FacetedSearchResultList-facetSearchResultList.newFacetSearch.Report_Entry")))

    # Fetch and parse HTML content
    log('Fetching and parsing HTML...')
    html_page = wd.page_source
    wd.quit()
    soup = BeautifulSoup(html_page, 'lxml')

    # Get relevant jobs
    log('Looking for relevant jobs...')
    job_soup = soup.find('div', {
                         'id': 'wd-FacetedSearchResultList-facetSearchResultList.newFacetSearch.Report_Entry'})

    roles_soup = job_soup.find_all('div', class_='gwt-Label')

    roles = []
    for role in roles_soup:
        # if(('WOC' in role.get_text() and '2021' in role.get_text()) or ('SWAP' in role.get_text() and '2021' in role.get_text())):
        if('Instructor' in role.get_text()):
            roles.append(role.get_text())

    return(roles)


if(is_connected()):
    try:
        log('Internet connection available.')
        relevant_roles = check_relevant_roles()

        if(relevant_roles):
            log(f'{len(relevant_roles)} relevant roles(s) found.')

            # Send mail

        else:
            log('No relevant roles found')

    except Exception as e:
        log(f'Error: {str(e)}.')

        # try:
        # Send error mail

        # If error mail cant be sent
        # except Exception as e:

else:
    log('No internet connection.')
