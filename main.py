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


def access_config_and_state():
    """retrieve the config & state items from config.json & state.json"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    parser.add_argument('-s', '--state', help='State file')
    args = parser.parse_args()

    if args.config and args.state:
        with open(args.config) as config_input, open(args.state) as state_input:
            config = json.load(config_input)
            state = json.load(state_input)
    else:
        print("Missing config or state file")
        sys.exit()

    return config, state


def get_last_updated_attribute(endpoint):
    """get the attribute name in each endpoint data that represent the last_updated timestamp"""

    # emulating switch/case statement
    return {
        'repositories': lambda: '',
        'branches': lambda: '',
        'commits': lambda: 'committer_date'
    }.get(endpoint, lambda: None)()


def update_state_file(endpoint, row_data):
    """to update the last_updated attribute value in state.json"""

    # retrieve state items from state.json
    _, state_items = access_config_and_state()

    # retrieve last_updated attribute name for selected endpoint
    last_updated = get_last_updated_attribute(endpoint)

    if last_updated in row_data:
        if row_data[last_updated] > state_items["bookmarks"][endpoint]['last_updated']:
            with open('state.json', 'w+') as state_file:
                state_items["bookmarks"][endpoint]['last_updated'] = row_data[last_updated]
                state_file.write(json.dumps(state_items))
    
    return None


def get_query_parameter(endpoint):
    """define the query parameter per endpoint"""

    # retrieve state items from state.json
    _, state_items = access_config_and_state()

    # emulating switch/case statement
    return {
        'repositories': lambda: '',
        'branches': lambda: '',
        'commits': lambda: f'&since={state_items["bookmarks"]["commits"]["last_updated"]}'
    }.get(endpoint, lambda: None)()


def get_complete_endpoint(endpoint, endpoint_params):
    """define the complete endpoint"""

    # retrieve config items from config.json
    config_items, _ = access_config_and_state()

    # emulating switch/case statement
    return {
        'repositories': lambda: f'users/{config_items["username"]}/repos',
        'branches': lambda: f'repos/{config_items["username"]}/{endpoint_params}/branches',
        'commits': lambda: f'repos/{config_items["username"]}/{endpoint_params}/commits'
    }.get(endpoint, lambda: None)()


def fetch_data_from_url(endpoint, endpoint_params, page):
    """fetch data for 1 page"""

    # retrieve config items from config.json
    config_items, _ = access_config_and_state()

    # try to fetch data, terminate program if failed
    try:
        response = requests.get(f'{config_items["base_api_url"]}/{get_complete_endpoint(endpoint, endpoint_params)}?page={page}{get_query_parameter(endpoint)}',
                                auth=(config_items["username"], config_items["access_token"])).json()
    except RequestException as error:
        print('an error occured: ', error)
        sys.exit()

    return response


def fetch_and_clean_thru_pages(endpoint, endpoint_params=None, page=1):
    """use function fetch_data_from_url() to loop thru all the pages"""

    # retrieve config items from config.json
    config_items, _ = access_config_and_state()

    # loop while page content is not empty
    while len(fetch_data_from_url(endpoint, endpoint_params, page)) > 0:
        response = fetch_data_from_url(endpoint, endpoint_params, page)

        # cleaning raw data
        cleaned_results = [handle_error_cleaning_pipeline(
            row, endpoint, endpoint_params) for row in response]

        # loop for every row in page
        for cleaned_result in cleaned_results:

            # update the state.json file to get the latest updated date if this is not the initial extraction
            None if config_items["is_initial_extraction"] == True else update_state_file(endpoint, cleaned_result)

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

# print(fetch_and_clean_thru_pages(endpoint))
# fetch_and_clean_thru_pages(endpoint)
