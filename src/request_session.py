from requests import Session
import sys
from urllib.parse import urljoin
from src.config_and_state import get_config_item

class RequestSession(Session):
    """Extension of Session to issue requests to GitLab."""
    def __init__(self, base_api: str, access_token: str, username: str):
        self.base_api = base_api
        self.access_token = access_token
        self.username = username
        Session.__init__(self)

    def request(self, method, url, params=None, *args, **kwargs):
        # prefix the URL with the appropriate base API url
        url = urljoin(self.base_api, f'/{url}')

        # inject the access_token & username
        if params is None:
            params = { 
                'access_token': self.access_token,
                'username': self.username
                }
        elif type(params) == dict:
            if 'access_token' not in params:
                params['access_token'] = self.access_token
            if 'username' not in params:
                params['username'] = self.username
        else:
            raise NotImplementedError('params is of unknown type (only dict supported)')

        return Session.request(self, method, url, params, *args, **kwargs)

request_session = RequestSession(
    get_config_item("base_api_url"),
    get_config_item("access_token"),
    get_config_item("username"),
)
