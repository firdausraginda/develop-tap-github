import requests
import argparse
import sys
import json
from data_cleansing import handle_error_cleaning_pipeline
from requests.exceptions import RequestException
from config_and_state import get_config_item, get_state_item, update_staging_state_file
from urllib.parse import urljoin


def dump_json(json_data):
    """dump data into a json file"""

    with open('dummy.json', 'w') as outfile:
        json.dump(json_data, outfile)

    return None


def check_initial_extraction(endpoint, is_updating_state):
    """to prevent system to extract data from the latest updated date in state.json if this is initial extraction"""

    return '' if get_config_item("is_initial_extraction") or is_updating_state == False else f'&since={get_state_item(endpoint, "last_updated_final")}'


def get_query_parameter(endpoint, page, is_updating_state):
    """define the query parameter per endpoint"""

    # emulating switch/case statement
    return {
        'repositories': lambda: f'page={page}{check_initial_extraction(endpoint, is_updating_state)}',
        'branches': lambda: f'page={page}',
        'commits': lambda: f'page={page}{check_initial_extraction(endpoint, is_updating_state)}'
    }.get(endpoint, lambda: None)()


def get_complete_endpoint(endpoint, endpoint_params):
    """define the complete endpoint"""

    # emulating switch/case statement
    return {
        'repositories': lambda: f'users/{get_config_item("username")}/repos',
        'branches': lambda: f'repos/{get_config_item("username")}/{endpoint_params}/branches',
        'commits': lambda: f'repos/{get_config_item("username")}/{endpoint_params}/commits'
    }.get(endpoint, lambda: None)()


def fetch_data_from_url(endpoint, endpoint_params, page, is_updating_state):
    """fetch data for 1 page"""

    # set the auth
    auth = get_config_item("username"), get_config_item("access_token")

    # join between base url, endpoint path, & query parameter
    complete_url = urljoin(get_config_item("base_api_url"), f'/{get_complete_endpoint(endpoint, endpoint_params)}?{get_query_parameter(endpoint, page, is_updating_state)}')

    # try to fetch data, terminate program if failed
    try:
        response = requests.get(complete_url, auth=auth).json()
    except RequestException as error:
        print('an error occured: ', error)
        sys.exit()
    return response


def fetch_and_clean_thru_pages(endpoint, endpoint_params=None, page=1, is_updating_state=True):
    """use function fetch_data_from_url() to loop thru all the pages"""

    # loop while page content is not empty
    while len(fetch_data_from_url(endpoint, endpoint_params, page, is_updating_state)) > 0:
        response = fetch_data_from_url(
            endpoint, endpoint_params, page, is_updating_state)

        # cleaning raw data
        cleaned_results = [handle_error_cleaning_pipeline(
            row, endpoint, endpoint_params) for row in response]

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


# dump_json(fetch_and_clean_thru_pages(
#     'commits', 'extracting-using-singer-spec'))

# dump_json(fetch_and_clean_thru_pages(
#     'branches', 'extracting-using-singer-spec'))

# dump_json(fetch_and_clean_thru_pages('repositories'))

# print(fetch_and_clean_thru_pages('repositories'))
# fetch_and_clean_thru_pages('repositories')
