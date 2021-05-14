from main import fetch_and_clean_thru_pages
import singer

# define schema
schema = {
    'properties': {
        'branch_name': {'type': 'string'},
        'repository_name': {'type': 'string'},
    },
    'required': ['branch_name']
}

# write schema
singer.write_schema('branch', schema, ['branch_name'])

# write records
for repos_data in fetch_and_clean_thru_pages('repos'):
    for branch_data in fetch_and_clean_thru_pages('branch', repos_data['repository_name']):
        singer.write_records('branch', [
            {
                'branch_name': branch_data['branch_name'],
                'repository_name': branch_data['repository_name'],
            }
        ])
