import requests
import argparse
import sys
import json
from data_cleansing import clean_pipeline

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
        sys.exit(1)
    
    return config['api_url'], config['username'], config['access_token']

def fetch_data_from_url(endpoint, page=1):
    """fetch data from the given URL using pre-defined auth access"""

    # get the api_url, username, & token from config.json
    api_url, auth_username, auth_token = access_config()

    return requests.get(f'{api_url}/{endpoint}?page={page}', auth=(auth_username, auth_token)).json()

def loop_thru_pages(endpoint, page=1):
    """use function fetch_data_from_url() to loop thru all the pages"""

    # loop while page content is not empty
    while len(fetch_data_from_url(endpoint, page)) > 0:
        response = fetch_data_from_url(endpoint, page)

        # cleaning raw data
        cleaned_results = [clean_pipeline(row, endpoint) for row in response]
     
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
# endpoint = 'users/firdausraginda/repos'

# dump_json(loop_thru_pages(endpoint))
# print(loop_thru_pages(endpoint))
# loop_thru_pages(endpoint)