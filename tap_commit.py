from main import fetch_and_clean_thru_pages
import singer

# define schema
schema = {
    'properties': {
        'url': {'type': 'string'},
        'repository_name': {'type': 'string'},
    },
    'required': ['url']
}

# write schema
singer.write_schema('commit', schema, ['url'])

# write records
for repos_data in fetch_and_clean_thru_pages('repos'):
    for commit_data in fetch_and_clean_thru_pages('commit', repos_data['repository_name']):
        singer.write_records('commit', [
            {
                'url': commit_data['url'],
                'repository_name': commit_data['repository_name'],
            }
        ])