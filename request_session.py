from collections.abc import Mapping
from requests import Session
import sys
from urllib.parse import urljoin
from config_and_state import get_config_item

class RequestSession(Session):
    """Extension of Session to issue requests to GitLab."""
    def __init__(self, instance_url: str, access_token: str):
        self.instance_url = instance_url
        self.access_token = access_token
        super(RequestSession, self).__init__()

    def request(self, method, url, params=None, *args, **kwargs):
        # Prefix the URL with the appropriate base.
        url = urljoin(self.instance_url, f'/api/v4{url}')

        # Inject the access token.
        if params is None:
            params = { 'access_token': self.access_token }
        elif isinstance(params, Mapping):
            if 'access_token' not in params:
                params['access_token'] = self.access_token
        else:
            raise NotImplementedError('params is of unknown type (only dict supported)')

        return super(RequestSession, self).request(method, url, params, *args, **kwargs)

request_session = RequestSession(
    get_config_item("base_api_url"),
    get_config_item("access_token"),
)
