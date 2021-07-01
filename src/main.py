import requests
import argparse
import sys
import json
from requests.exceptions import RequestException
from urllib.parse import urljoin
from src.data_cleansing import handle_error_cleaning_pipeline
from src.config_and_state import get_config_item, get_state_item, update_staging_state_file
import time
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)

def check_initial_extraction(endpoint, is_updating_state):
    """to prevent system to extract data from the latest updated date in state.json if this is initial extraction"""

    return None if get_config_item("is_initial_extraction") or is_updating_state == False else get_state_item(endpoint, "last_updated_final")


def get_since_param_pipeline(endpoint, is_updating_state):
    """define the query parameter per endpoint"""

    # emulating switch/case statement
    return {
        'repositories': lambda: check_initial_extraction(endpoint, is_updating_state),
        'branches': lambda: None,
        'commits': lambda: check_initial_extraction(endpoint, is_updating_state)
    }.get(endpoint, lambda: None)()


def get_complete_endpoint_url(endpoint, repository_name):
    """define the complete endpoint"""

    # emulating switch/case statement
    return {
        'repositories': lambda: f'users/{get_config_item("username")}/repos',
        'branches': lambda: f'repos/{get_config_item("username")}/{repository_name}/branches',
        'commits': lambda: f'repos/{get_config_item("username")}/{repository_name}/commits'
    }.get(endpoint, lambda: None)()


def fetch_data_from_url(endpoint, repository_name, page, is_updating_state):
    """func to set the auth, headers, params, url, & instantiate request session. This func will fetch data in 1 page"""

    # set auth. Can be a substitue of an access_token
    auth = (get_config_item('my_client_id'), get_config_item('my_client_secret'))
    
    # set headers
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': get_config_item('access_token'),
    }

    # set params
    params = {
        'username': get_config_item('username'),
        'page': page,
        'since': get_since_param_pipeline(endpoint, is_updating_state),
    }

    # set url
    url = urljoin(get_config_item('base_api_url'), f'/{get_complete_endpoint_url(endpoint, repository_name)}')

    # instantiate request session
    session = requests.Session()

    is_api_calls_succeed = False

    while not is_api_calls_succeed:
        # try to fetch data, wait for 10s if failed, then try again
        try:
            response = session.get(url=url, auth=auth, params=params).json()
            is_api_calls_succeed = True
        except Exception as err:
            print('an error occured: ', err)
            time.sleep(10)
            # sys.exit(1)
    
    return response


def fetch_and_clean_thru_pages(endpoint, repository_name=None, page=1, is_updating_state=True):
    """use function fetch_data_from_url() to loop thru all the pages"""

    # loop while page content is not empty
    while len(fetch_data_from_url(endpoint, repository_name, page, is_updating_state)) > 0:
        response = fetch_data_from_url(
            endpoint, repository_name, page, is_updating_state)

        # cleaning raw data
        cleaned_results = [handle_error_cleaning_pipeline(
            row, endpoint, repository_name) for row in response]

        # loop for every row in page
        for cleaned_result in cleaned_results:

            # update the state.json file to get the latest updated date if this is a parent loop e.g. repositories of commits
            None if is_updating_state == False else update_staging_state_file(
                endpoint, cleaned_result)

            # yield the cleaned data per API page
            yield cleaned_result

        # ternary operator to append list if current iteration is not on the 1st page
        # temp_result = cleaned_results if page == 1 else temp_result + cleaned_results

        page += 1

    return None
