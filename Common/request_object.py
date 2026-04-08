from requests.auth import AuthBase
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BearerAuth(AuthBase):
    """A class representing Bearer Token Auth object

    Args:
        AuthBase (_type_): _description_
    """

    def __init__(self, token) -> None:
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r


class Session:
    """
    A class representing a base session.

    Attributes:
    - DEFAULT_TOKEN (str): The default authentication token.
    - authen_token (BearerAuth): The authentication token.
    - url (str): The URL of the server.

    Methods:
    - __init__(self, token:str=DEFAULT_TOKEN, url:str='https://sd.homecredit.vn/rest/api/2/'): Initializes a JIRA session object.
    - get_request(self, endpoint:str): Sends a GET request to the specified endpoint.
    """

    # BASIC FUNCTION FOR ONE SESSION
    # This include initiation of the session, base function for get_request and post_request

    def __init__(
        self,
        token: str,
        url: str,
        auth_type: str = "bearer"
    ):
        """
        Initializes a request session object.

        Parameters:
        - token (str): The authentication token. Defaults to DEFAULT_TOKEN.
        - url (str): The URL of the intended server
        """
        self.url = url
        self.token = token
        if auth_type.lower() == "bearer":
            self.authen_token = BearerAuth(token)
        elif auth_type.lower() == "basic":
            self.authen_token = f"{token}"
        else:
            raise ValueError("Invalid auth_type. Use 'bearer' or 'basic'.")

    def get_request(self, endpoint: str) -> requests.models.Response:
        """
        Sends a GET request to the specified endpoint.

        Parameters:
        - endpoint (str): The endpoint to send the request to.

        Returns:
        - result: The result of the GET request.
        """
        if isinstance(self.authen_token, BearerAuth):
            result = requests.get(
                self.url + endpoint, auth=self.authen_token, timeout=10)
        elif isinstance(self.authen_token, str):
            result = requests.get(self.url + endpoint,
                                  headers={"Authorization": f"{self.authen_token}"}, timeout=10, verify=False)
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
        if isinstance(self.authen_token, BearerAuth):
            result = requests.post(
                self.url + endpoint, auth=self.authen_token, json=payload, timeout=10)
        elif isinstance(self.authen_token, str):
            result = requests.post(
                self.url + endpoint, headers={"Authorization": f"{self.authen_token}"}, json=payload, timeout=10, verify=False)
        return result

    def patch_request(self, endpoint: str, payload) -> requests.models.Response:
        """
        Sends a POST request to the specified endpoint with the given payload.

        Parameters:
        - endpoint (str): The endpoint to send the request to.
        - payload: The payload to include in the request.

        Returns:
        - result: The response object received from the server.
        """
        if isinstance(self.authen_token, BearerAuth):
            result = requests.patch(
                self.url + endpoint, auth=self.authen_token, json=payload, timeout=10)
        elif isinstance(self.authen_token, str):
            result = requests.patch(
                self.url + endpoint, headers={"Authorization": f"{self.authen_token}"}, json=payload, timeout=30, verify=False)
        return result

    def delete_request(self, endpoint: str, payload) -> requests.models.Response:
        """
        Sends a DELETE request to the specified endpoint with the given payload.

        Args:
        - endpoint (str): The endpoint to send the request to.
        - payload: The payload to include in the request.

        Returns:
            requests.models.Response: _description_
        """
        if isinstance(self.authen_token, BearerAuth):
            result = requests.delete(
                self.url + endpoint, auth=self.authen_token, json=payload, timeout=10)
        elif isinstance(self.authen_token, str):
            result = requests.delete(
                self.url + endpoint, headers={"Authorization": f"{self.authen_token}"}, json=payload, timeout=10, verify=False)
        return result
