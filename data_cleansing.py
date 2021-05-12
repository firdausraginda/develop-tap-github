def flatten_nested_dict(prefix, nested_dict):
    
    cleaned_nested_dict = {}
    
    for key,val in nested_dict.items():
        cleaned_nested_dict[f'{prefix}_{key}'] = val
    
    return cleaned_nested_dict

def handle_empty_string(item):
    string_converted = str(item)
    return None if len(string_converted.strip()) == 0 else string_converted.strip()

def clean_pipeline(raw_data, endpoint, endpoint_params):
    """select function based on data endpoint"""

    # emulating switch/case statement
    return {
        'repos': clean_repo,
        'branch': clean_branch
    }.get(endpoint, lambda: None)(raw_data, endpoint_params)

def clean_repo(raw_data, endpoint_params):
    """clean repository data"""

    cleaned_dict = {}
    cleaned_dict['id'] = handle_empty_string(raw_data['id'])
    cleaned_dict['repository_name'] = handle_empty_string(raw_data['name'])
    cleaned_dict['is_private'] = raw_data['private']

    owner_nested = flatten_nested_dict(prefix = 'owner', nested_dict = raw_data['owner'])
    cleaned_dict['owner_id'] = handle_empty_string(owner_nested['owner_id'])
    cleaned_dict['owner_name'] = handle_empty_string(owner_nested['owner_login'])
    cleaned_dict['owner_avatar_url'] = handle_empty_string(owner_nested['owner_avatar_url'])
    cleaned_dict['owner_api_url'] = handle_empty_string(owner_nested['owner_url'])
    cleaned_dict['owner_html_url'] = handle_empty_string(owner_nested['owner_html_url'])
    cleaned_dict['owner_type'] =handle_empty_string( owner_nested['owner_type'])

    cleaned_dict['api_url'] = handle_empty_string(raw_data['url'])
    cleaned_dict['html_url'] = handle_empty_string(raw_data['html_url'])
    cleaned_dict['description'] = handle_empty_string(raw_data['description'])
    cleaned_dict['created_at'] = raw_data['created_at']
    cleaned_dict['updated_at'] = raw_data['updated_at']
    cleaned_dict['pushed_at'] = raw_data['pushed_at']
    cleaned_dict['git_url'] = handle_empty_string(raw_data['git_url'])
    cleaned_dict['ssh_url'] = handle_empty_string(raw_data['ssh_url'])
    cleaned_dict['size'] = raw_data['size']
    cleaned_dict['stargazers_count'] = raw_data['stargazers_count']
    cleaned_dict['watchers_count'] = raw_data['watchers_count']
    cleaned_dict['language'] = handle_empty_string(raw_data['language'])
    cleaned_dict['is_archived'] = raw_data['archived']

    return cleaned_dict

def clean_branch(raw_data, endpoint_params):
    """clean branch data"""

    cleaned_dict = {}
    cleaned_dict['branch_name'] = handle_empty_string(raw_data['name'])
    cleaned_dict['repository_name'] = handle_empty_string(endpoint_params)

    return cleaned_dict

