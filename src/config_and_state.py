import argparse
import sys
import json
from datetime import datetime
from datetime import timedelta
import os


def last_updated_date_added_1_second(RFC3339_format):
    """add 1 second to final last updated date (state.json file)"""

    # standardizing to normal datetime
    standardized_datetime = datetime.strptime(
        str(RFC3339_format), "%Y-%m-%dT%H:%M:%SZ")

    # add 1 second
    added_1_second = standardized_datetime + timedelta(seconds=1)

    # convert back to RFC3339 date format
    converted_to_is_datetime = datetime.strftime(
        added_1_second, "%Y-%m-%dT%H:%M:%SZ")

    return converted_to_is_datetime


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
        sys.exit(1)

    return config, state


def get_config_item(item):
    config_items, _ = access_config_and_state()
    return config_items[item]


def get_state_item(endpoint, item):
    _, state_items = access_config_and_state()
    return state_items["bookmarks"][endpoint][item]


def get_last_updated_attribute(endpoint):
    """get the attribute name in each endpoint data that represent the last_updated timestamp"""

    # emulating switch/case statement
    return {
        'repositories': lambda: 'updated_at',
        'branches': lambda: '',
        'commits': lambda: 'committer_date'
    }.get(endpoint, lambda: None)()


def update_final_state_file(endpoint):

    # retrieve state items from state.json
    _, state_items = access_config_and_state()

    last_updated_staging_item = get_state_item(
        endpoint, 'last_updated_staging')

    path_to_state = os.path.join(os.path.dirname(__file__), '../state.json')

    with open(path_to_state, 'w+') as state_file:
        state_items["bookmarks"][endpoint]['last_updated_final'] = last_updated_date_added_1_second(
            last_updated_staging_item)
        state_file.write(json.dumps(state_items))

    return None


def update_staging_state_file(endpoint, row_data):
    """to update the last_updated attribute value in state.json"""

    # retrieve state items from state.json
    _, state_items = access_config_and_state()

    # retrieve last_updated attribute name for selected endpoint
    last_updated = get_last_updated_attribute(endpoint)

    path_to_state = os.path.join(os.path.dirname(__file__), '../state.json')

    if last_updated in row_data:
        if row_data[last_updated] > get_state_item(endpoint, "last_updated_staging"):
            with open(path_to_state, 'w+') as state_file:
                state_items["bookmarks"][endpoint]['last_updated_staging'] = row_data[last_updated]
                state_file.write(json.dumps(state_items))

    return None
