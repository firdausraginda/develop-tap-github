import sys


def flatten_nested_dict(prefix, nested_dict):
    """flatenning 1 level of nested dictionary"""

    cleaned_nested_dict = {}
    cleaned_nested_dict = {
        f'{prefix}_{key}': val for key, val in nested_dict.items()}

    return cleaned_nested_dict


def handle_empty_string(item):
    """set empty string to null value"""

    convert_to_string = str(item)

    return None if len(convert_to_string.strip()) == 0 or convert_to_string == 'None' else convert_to_string.strip()


def handle_empty_list(item):
    """set empty list to null value"""

    return None if len(item) == 0 else item


def handle_error_cleaning_pipeline(raw_data, endpoint, endpoint_params):
    """use try & except to handle error while cleaning data"""

    try:
        result = clean_pipeline(raw_data, endpoint, endpoint_params)
    except Exception as e:
        print(f'Error! data doesn\'t exist while cleansing proccess running!')
        print(e)
        sys.exit(1)

    return result


def clean_pipeline(raw_data, endpoint, endpoint_params):
    """mapped function based on data endpoint"""

    # emulating switch/case statement
    return {
        'repositories': clean_repo,
        'branches': clean_branch,
        'commits': clean_commit,
    }.get(endpoint, lambda: None)(raw_data, endpoint_params)


def clean_repo(raw_data, endpoint_params):
    """cleaning repository data"""

    cleaned_dict = {}

    cleaned_dict['id'] = handle_empty_string(raw_data['id'])
    cleaned_dict['repository_name'] = handle_empty_string(raw_data['name'])
    cleaned_dict['is_private'] = raw_data['private']

    owner_nested = flatten_nested_dict('owner', raw_data['owner'])
    cleaned_dict['owner_id'] = handle_empty_string(owner_nested['owner_id'])
    cleaned_dict['owner_name'] = handle_empty_string(
        owner_nested['owner_login'])
    cleaned_dict['owner_avatar_url'] = handle_empty_string(
        owner_nested['owner_avatar_url'])
    cleaned_dict['owner_api_url'] = handle_empty_string(
        owner_nested['owner_url'])
    cleaned_dict['owner_html_url'] = handle_empty_string(
        owner_nested['owner_html_url'])
    cleaned_dict['owner_type'] = handle_empty_string(
        owner_nested['owner_type'])

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
    """cleaning branch data"""

    cleaned_dict = {}

    cleaned_dict['branch_name'] = handle_empty_string(raw_data['name'])
    cleaned_dict['repository_name'] = handle_empty_string(endpoint_params)

    commit_nested = flatten_nested_dict('commit', raw_data['commit'])
    cleaned_dict['commit_url'] = handle_empty_string(
        commit_nested['commit_url'])
    cleaned_dict['commit_sha'] = handle_empty_string(
        commit_nested['commit_sha'])

    cleaned_dict['protected'] = raw_data['protected']

    return cleaned_dict


def clean_commit(raw_data, endpoint_params):
    """cleaning commit data"""

    cleaned_dict = {}

    cleaned_dict['url'] = handle_empty_string(raw_data['url'])
    cleaned_dict['repository_name'] = handle_empty_string(endpoint_params)
    cleaned_dict['sha'] = handle_empty_string(raw_data['sha'])
    cleaned_dict['html_url'] = handle_empty_string(raw_data['html_url'])
    cleaned_dict['comments_url'] = handle_empty_string(
        raw_data['comments_url'])

    commit_nested = flatten_nested_dict('commit', raw_data['commit'])
    cleaned_dict['api_url'] = handle_empty_string(commit_nested['commit_url'])
    cleaned_dict['message'] = handle_empty_string(
        commit_nested['commit_message'])
    cleaned_dict['comment_count'] = commit_nested['commit_comment_count']

    commit_author_nested = flatten_nested_dict(
        'commit_author', raw_data['commit']['author'])
    cleaned_dict['author_email'] = handle_empty_string(
        commit_author_nested['commit_author_email'])
    cleaned_dict['author_date'] = handle_empty_string(
        commit_author_nested['commit_author_date'])

    commit_committer_nested = flatten_nested_dict(
        'commit_committer', raw_data['commit']['committer'])
    cleaned_dict['committer_email'] = handle_empty_string(
        commit_committer_nested['commit_committer_email'])
    cleaned_dict['committer_date'] = handle_empty_string(
        commit_committer_nested['commit_committer_date'])

    commit_tree_nested = flatten_nested_dict(
        'commit_tree', raw_data['commit']['tree'])
    cleaned_dict['tree_url'] = handle_empty_string(
        commit_tree_nested['commit_tree_url'])
    cleaned_dict['tree_sha'] = handle_empty_string(
        commit_tree_nested['commit_tree_sha'])

    commit_verification_nested = flatten_nested_dict(
        'commit_verification', raw_data['commit']['verification'])
    cleaned_dict['verification_verified'] = commit_verification_nested['commit_verification_verified']
    cleaned_dict['verification_reason'] = handle_empty_string(
        commit_verification_nested['commit_verification_reason'])
    cleaned_dict['verification_signature'] = handle_empty_string(
        commit_verification_nested['commit_verification_signature'])
    cleaned_dict['verification_payload'] = handle_empty_string(
        commit_verification_nested['commit_verification_payload'])

    return cleaned_dict
