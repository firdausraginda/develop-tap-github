from src.main import fetch_and_clean_thru_pages
from src.config_and_state import update_final_state_file
import singer

# define schema
schema = {
    'properties': {
        'id': {'type': 'string'},
        'repository_name': {'type': 'string'},
        'is_private': {'type': 'boolean'},
        'owner_id': {'type': 'string'},
        'owner_name': {'type': 'string'},
        'owner_avatar_url': {'type': 'string'},
        'owner_api_url': {'type': 'string'},
        'owner_html_url': {'type': 'string'},
        'api_url': {'type': 'string'},
        'html_url': {'type': 'string'},
        'description': {'type': 'string'},
        'created_at': {'type': 'string', 'format': 'date-time'},
        'updated_at': {'type': 'string', 'format': 'date-time'},
        'pushed_at': {'type': 'string', 'format': 'date-time'},
        'git_url': {'type': 'string'},
        'ssh_url': {'type': 'string'},
        'size': {'type': 'integer'},
        'stargazers_count': {'type': 'integer'},
        'watchers_count': {'type': 'integer'},
        'language': {'type': 'string'},
        'is_archived': {'type': 'boolean'},
    },
    'required': ['id', 'owner_id']
}

# write schema
singer.write_schema('repository_logs', schema, ['id', 'owner_id'])

counter = 0

# write records
for result_data in fetch_and_clean_thru_pages('repositories'): 
    singer.write_records('repository_logs', [
        {
            'id': result_data['id'],
            'repository_name': result_data['repository_name'],
            'is_private': result_data['is_private'],

            'owner_id': result_data['owner_id'],
            'owner_name': result_data['owner_name'],
            'owner_avatar_url': result_data['owner_avatar_url'],
            'owner_api_url': result_data['owner_api_url'],
            'owner_html_url': result_data['owner_html_url'],

            'api_url': result_data['api_url'],
            'html_url': result_data['html_url'],
            'description': result_data['description'],
            'created_at': result_data['created_at'],
            'updated_at': result_data['updated_at'],
            'pushed_at': result_data['pushed_at'],
            'git_url': result_data['git_url'],
            'ssh_url': result_data['ssh_url'],
            'size': result_data['size'],
            'stargazers_count': result_data['stargazers_count'],
            'watchers_count': result_data['watchers_count'],
            'language': result_data['language'],
            'is_archived': result_data['is_archived'],
        }
    ])

    counter += 1
    print(counter)

# update the last_updated_final in state.json file
update_final_state_file('repositories')