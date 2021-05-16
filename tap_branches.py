from main import fetch_and_clean_thru_pages
import singer

# define schema
schema = {
    'properties': {
        'branch_name': {'type': 'string'},
        'repository_name': {'type': 'string'},
        'commit_url': {'type': 'string'},
        'commit_sha': {'type': 'string'},
        'protected': {'type': 'string'},
        'protection_required_status_checks_enforcement_level': {'type': 'string'},
        'protection_required_status_checks_contexts': {'type': 'string'},
    },
    'required': ['branch_name']
}

# write schema
singer.write_schema('branches', schema, ['branch_name'])

# write records
for repos_data in fetch_and_clean_thru_pages('repositories'):
    for branch_data in fetch_and_clean_thru_pages('branches', repos_data['repository_name']):
        singer.write_records('branches', [
            {
                'branch_name': branch_data['branch_name'],
                'repository_name': branch_data['repository_name'],
                'commit_url': branch_data['commit_url'],
                'commit_sha': branch_data['commit_sha'],
                'protected': branch_data['protected'],
                'protection_required_status_checks_enforcement_level': branch_data['protection_required_status_checks_enforcement_level'],
                'protection_required_status_checks_contexts': branch_data['protection_required_status_checks_contexts'],
            }
        ])
