from src.main import fetch_and_clean_thru_pages
from src.config_and_state import update_final_state_file
import singer

# define schema
schema = {
    'properties': {
        'url': {'type': 'string'},
        'repository_name': {'type': 'string'},
        'sha': {'type': 'string'},
        'html_url': {'type': 'string'},
        'comments_url': {'type': 'string'},
        'api_url': {'type': 'string'},
        'message': {'type': 'string'},
        'comment_count': {'type': 'integer'},
        'author_email': {'type': 'string'},
        'author_date': {'type': 'string'},
        'committer_email': {'type': 'string'},
        'committer_date': {'type': 'string'},
        'tree_url': {'type': 'string'},
        'tree_sha': {'type': 'string'},
        'verification_verified': {'type': 'boolean'},
        'verification_reason': {'type': 'string'},
        'verification_signature': {'type': 'string'},
        'verification_payload': {'type': 'string'},
    },
    'required': ['url']
}

# write schema
singer.write_schema('commit_logs', schema, ['url'])

counter = 0

# write records
for repos_data in fetch_and_clean_thru_pages('repositories', is_updating_state=False):
    for commit_data in fetch_and_clean_thru_pages('commits', repos_data['repository_name']):
        singer.write_records('commit_logs', [
            {
                'url': commit_data['url'],
                'repository_name': commit_data['repository_name'],
                'sha': commit_data['sha'],
                'html_url': commit_data['html_url'],
                'comments_url': commit_data['comments_url'],
                'api_url': commit_data['api_url'],
                'message': commit_data['message'],
                'comment_count': commit_data['comment_count'],
                'author_email': commit_data['author_email'],
                'author_date': commit_data['author_date'],
                'committer_email': commit_data['committer_email'],
                'committer_date': commit_data['committer_date'],
                'tree_url': commit_data['tree_url'],
                'tree_sha': commit_data['tree_sha'],
                'verification_verified': commit_data['verification_verified'],
                'verification_reason': commit_data['verification_reason'],
                'verification_signature': commit_data['verification_signature'],
                'verification_payload': commit_data['verification_payload'],
            }
        ])

        counter += 1
        print(counter)

# update the last_updated_final in state.json file
update_final_state_file('commits')