import requests
import json
from requests.auth import AuthBase
from requests.models import Response


class BearerAuth(AuthBase):
    """
    BearerAuth is a class that implements the authentication mechanism using a bearer token.
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

class Session:
    """
    A class representing a base session.

    Attributes:
    - DEFAULT_TOKEN (str): The default authentication token.
    - authen_token (BearerAuth): The authentication token.
    - url (str): The URL of the JIRA server.

    Methods:
    - __init__(self, token:str=DEFAULT_TOKEN, url:str='https://servicedesk.homecredit.net/rest/api/2/'): Initializes a JIRA session object.
    - get_request(self, endpoint:str): Sends a GET request to the specified endpoint.
    - parse_ticket(self, result): Parses the result of a ticket request.
    - browse_ticket(self, ticket_key:str): Retrieves and parses a specific ticket.
    """

    # _DEFAULT_TOKEN = "NzE3ODQ3NDAyMDY2Om6ftk+Eq6PvvpA7brQqQX/ICKnq"
    # _POC3_TOKEN = "NzgxMTcyMjA5NjA4OhnMqkkjUL4yQJeZimk3LSppxCPB"
    # poc3_url = "https://jira-servicedesk-poc3.cz.infra/rest/api/2/"
    # This DEFAULT_TOKEN is for the HCVN Service Desk account.
    _DEFAULT_TOKEN = "MTk1MDYwMDk4OTA2OhXn7u7wkG9wQ3N7fiaW1tMCkyQb"
    authen_token = BearerAuth(_DEFAULT_TOKEN)
    url = ""

    # DEFAULT cURL for JIRA API
    _DEFAULT_URL = "https://servicedesk.homecredit.net/rest/api/2/"
    _BROWSE_TICKET = "issue/"
    _JQL_SEARCH = "search?jql="
    _TRANSITION = "issue/{ticket_key}/transitions"


    # BASIC FUNCTION FOR ONE SESSION
    # This include initiation of the session, base function for get_request and post_request
    def __init__(
        self,
        token: str = _DEFAULT_TOKEN,
        url: str = _DEFAULT_URL,
    ):
        """
        Initializes a JIRA session object.

        Parameters:
        - token (str): The authentication token. Defaults to DEFAULT_TOKEN.
        - url (str): The URL of the JIRA server. Defaults to 'https://servicedesk.homecredit.net/rest/api/2/'.
        """
        self.url = url
        self.token = token
        self.authen_token = BearerAuth(token)

    def get_request(self, endpoint: str) -> requests.models.Response:
        """
        Sends a GET request to the specified endpoint.

        Parameters:
        - endpoint (str): The endpoint to send the request to.

        Returns:
        - result: The result of the GET request.
        """
        result = requests.get(self.url + endpoint, auth=self.authen_token, timeout=10)
        return result


    def post_request(self, endpoint: str, payload) -> requests.models.Response:
        """
        Sends a POST request to the specified endpoint with the given payload.

        Parameters:
        - endpoint (str): The endpoint to send the request to.
        - payload: The payload to include in the request.

        Returns:
        - result: The response object received from the server.
        """
        result = requests.post(self.url + endpoint, auth=self.authen_token, json=payload, timeout=10)
        return result
        
        

def get_id_from_response(response: Response) -> dict:
    """This function is to support getting the ID from the response of the API

    Args:
        response (Response): Response from the API

    Returns:
        dict: ID from the response
    """
    return_dict = {}

    try:
        json_obj = json.loads(response.text)
        for fields in json_obj['transitions']:
            return_dict[fields['name']] = fields['id']
        return return_dict
    except Exception as e:  # noqa: E722
        print("File Error, file not found!\n")
        print(e)
        return {}  # Return an empty dictionary if an exception occurs
    

    