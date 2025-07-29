from brynq_sdk_brynq import BrynQ
from typing import Union, List, Literal, Optional
import requests


class NewRelicAPI(BrynQ):

    def __init__(self, system_type: Optional[Literal['source', 'target']] = None, debug: bool = False):
        """
        For the full documentation, see: https://docs.newrelic.com/docs/apis/nerdgraph/get-started/introduction-new-relic-nerdgraph/
        """
        super().__init__()
        self.headers = self._set_credentials(system_type)
        self.url = "https://api.newrelic.com/graphql"
        self.timeout = 3600

    def _set_credentials(self, system_type):
        """
        Get the credentials from BrynQ and get the username and private key from there
        """
        credentials = self.interfaces.credentials.get(system="newrelic-api", system_type=system_type)
        credentials = credentials.get('data')
        api_key = credentials['api_key']
        headers = {
                  'API-Key': f'{api_key}',
                  'Content-Type': 'application/json'
        }
        return headers

    def execute_query(self, query: dict):
        response = requests.post(self.url, headers=self.headers, json=query, timeout=self.timeout)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

        return response