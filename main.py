import requests
import argparse
import sys
import json

url = 'https://api.github.com'
endpoint = 'users'
endpoint_params = 'firdausraginda'

def access_config():
    """access & return the config items from config.json"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    args = parser.parse_args()

    if args.config:
        with open(args.config) as input:
            config = json.load(input)
    else:
        config = {}
        print("Missing Config file")
        print("'-c', '--config'")
        sys.exit(1)
    
    return config['username'], config['access_token']

def fetch_data_from_url(url, endpoint, endpoint_params):
    """fetch data from the given URL & params with the pre-defined auth access"""

    auth_username, auth_token = access_config()
    return requests.get(f'{url}/{endpoint}/{endpoint_params}', auth=(auth_username, auth_token)).json()

print(fetch_data_from_url(url, endpoint, endpoint_params))