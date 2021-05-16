import requests
import argparse
import sys
import json
from data_cleansing import handle_error_cleaning_pipeline
from requests.exceptions import RequestException

def dump_json(json_data):
    """dump data into a json file"""

    with open('dummy.json', 'w') as outfile:
        json.dump(json_data, outfile)

    return None

def access_config():
    """retrieve the config items from config.json"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    args = parser.parse_args()

    if args.config:
        with open(args.config) as input:
            config = json.load(input)
    else:
        config = {}
        print("Missing config file: '-c' or '--config")
        sys.exit()
    
    return config['base_api_url'], config['username'], config['access_token']

def get_complete_endpoint(endpoint, endpoint_params):
    """define the complete endpoint"""

    # get the base_api_url, username, & token from config.json
    base_api_url, auth_username, auth_token = access_config()
    
    # emulating switch/case statement
    return {
        'repos': lambda: f'users/{auth_username}/repos',
        'branch': lambda: f'repos/{auth_username}/{endpoint_params}/branches',
        'commit': lambda: f'repos/{auth_username}/{endpoint_params}/commits'
    }.get(endpoint, lambda: None)()

def fetch_data_from_url(endpoint, endpoint_params, page):
    """fetch data for 1 page"""

    # get the base_api_url, username, & token from config.json
    base_api_url, auth_username, auth_token = access_config()

    # try to fetch data, terminate program if failed
    try:
        response = requests.get(f'{base_api_url}/{get_complete_endpoint(endpoint, endpoint_params)}?page={page}', auth=(auth_username, auth_token)).json()
    except RequestException as error:
        print('an error occured: ', error)
        sys.exit()

    return response

def fetch_and_clean_thru_pages(endpoint, endpoint_params=None, page=1):
    """use function fetch_data_from_url() to loop thru all the pages"""

    # loop while page content is not empty
    while len(fetch_data_from_url(endpoint, endpoint_params, page)) > 0:
        response = fetch_data_from_url(endpoint, endpoint_params, page)
        
        # cleaning raw data
        cleaned_results = [handle_error_cleaning_pipeline(row, endpoint, endpoint_params) for row in response]
     
        # yield the cleaned data per API page
        for cleaned_result in cleaned_results:
            yield cleaned_result

        # ternary operator to append list if current iteration is not on the 1st page
        # temp_result = cleaned_result if page == 1 else temp_result + cleaned_result

        page += 1

    return None

# users
# endpoint = 'users'
# endpoint = 'users/firdausraginda'

# repo
# endpoint = 'repos/firdausraginda/basic-airflow/commits'

# dump_json(fetch_and_clean_thru_pages(endpoint))
# print(fetch_and_clean_thru_pages(endpoint))
# fetch_and_clean_thru_pages(endpoint)