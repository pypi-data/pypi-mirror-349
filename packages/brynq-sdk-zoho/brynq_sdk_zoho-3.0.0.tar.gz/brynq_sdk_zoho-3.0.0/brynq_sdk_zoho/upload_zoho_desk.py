import os
import sys
import pandas as pd
from typing import Union, List, Optional, Literal
import requests
import json
from brynq_sdk_brynq import BrynQ
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)


class UploadZohoDesk(BrynQ):

    def __init__(self, system_type: Optional[Literal['source', 'target']] = None, debug: bool = False):
        """
        For the full documentation, see: https://avisi-apps.gitbook.io/tracket/api/
        """
        super().__init__()
        self.headers = self._get_authentication(system_type)
        self.base_url = "https://desk.zoho.com/api/v1/"
        self.timeout = 3600

    def _get_authentication(self, system_type):
        """
        Get the credentials for the Traket API from BrynQ, with those credentials, get the access_token for Tracket.
        Return the headers with the access_token.
        """
        # Get credentials from BrynQ
        credentials = self.interfaces.credentials.get(system="zoho-desk", system_type=system_type)
        credentials = credentials.get('data')

        headers = {
            'Authorization': f'Zoho-oauthtoken {credentials.get("access_token")}',
            'Content-Type': 'application/json'
        }
        return headers

    def update_ticket_time_entry(self, ticket_id, time_entry_id, payload):
        """
        This function updates the time entry of a ticket in zoho desk
        :param ticket_id: str
        :param time_entry_id: str
        :param payload: dict
        """
        url = f"{self.base_url}tickets/{ticket_id}/timeEntry/{time_entry_id}"
        response = requests.request("PATCH", url, headers=self.headers, data=json.dumps(payload), timeout=self.timeout)
        return response
