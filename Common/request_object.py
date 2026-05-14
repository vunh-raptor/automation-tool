from requests.auth import AuthBase
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BearerAuth(AuthBase):
    """A class representing Bearer Token Auth object.
    
    Implements AuthBase to inject Bearer token into request headers.

    Args:
        AuthBase: requests authentication base class
    """

    def __init__(self, token: str) -> None:
        """Initialize with Bearer token.
        
        Parameters:
        - token (str): The Bearer token
        """
        self.token = token

    def __call__(self, r):
        """Apply Bearer authentication to request.
        
        Parameters:
        - r: requests.Request object
        
        Returns:
        - r: Modified request with Authorization header
        """
        r.headers["Authorization"] = "Bearer " + self.token
        return r


class BasicAuth(AuthBase):
    """A class representing Basic Auth object.
    
    Implements AuthBase to inject Basic auth token into request headers.
    Encapsulates the auth header-building logic for consistency with BearerAuth.

    Args:
        AuthBase: requests authentication base class
    """

    def __init__(self, token: str) -> None:
        """Initialize with Basic auth token (already base64-encoded 'Basic <token>').
        
        Parameters:
        - token (str): The pre-formatted Basic auth token (e.g., 'Basic base64encoded...')
        """
        self.token = token

    def __call__(self, r):
        """Apply Basic authentication to request.
        
        Parameters:
        - r: requests.Request object
        
        Returns:
        - r: Modified request with Authorization header
        """
        r.headers["Authorization"] = self.token
        return r


class Session:
    """
    A class representing a base session for making HTTP requests with authentication.

    Attributes:
    - url (str): The base URL of the server.
    - token (str): The raw authentication token.
    - authen_token (AuthBase): The authentication handler (BearerAuth or BasicAuth).
    - verify_ssl (bool): Whether to verify SSL certificates.

    Methods:
    - __init__(self, token:str, url:str, auth_type:str="bearer", verify_ssl:bool=False): Initializes session.
    - get_request(self, endpoint:str): Sends a GET request.
    - post_request(self, endpoint:str, payload): Sends a POST request.
    - patch_request(self, endpoint:str, payload): Sends a PATCH request.
    - delete_request(self, endpoint:str, payload): Sends a DELETE request.
    """

    def __init__(
        self,
        token: str,
        url: str,
        auth_type: str = "bearer",
        verify_ssl: bool = False
    ):
        """
        Initializes a request session object.

        Parameters:
        - token (str): The authentication token (raw Bearer token or 'Basic <base64>' string).
        - url (str): The base URL of the intended server.
        - auth_type (str): Type of authentication - 'bearer' or 'basic'. Defaults to 'bearer'.
        - verify_ssl (bool): Whether to verify SSL certificates. Defaults to False (disabled).
        
        Raises:
        - ValueError: If auth_type is not 'bearer' or 'basic'.
        """
        self.url = url
        self.token = token
        self.verify_ssl = verify_ssl
        
        # Dependency Injection: Select auth handler based on type. Eliminates branching in HTTP methods.
        auth_type_lower = auth_type.lower()
        if auth_type_lower == "bearer":
            self.authen_token = BearerAuth(token)
        elif auth_type_lower == "basic":
            self.authen_token = BasicAuth(token)
        else:
            raise ValueError("Invalid auth_type. Use 'bearer' or 'basic'.")

    def get_request(self, endpoint: str) -> requests.models.Response:
        """
        Sends a GET request to the specified endpoint.

        Parameters:
        - endpoint (str): The endpoint path to append to base URL.

        Returns:
        - requests.models.Response: The response from the server.
        """
        return requests.get(
            self.url + endpoint,
            auth=self.authen_token,
            timeout=10,
            verify=self.verify_ssl
        )

    def post_request(self, endpoint: str, payload) -> requests.models.Response:
        """
        Sends a POST request to the specified endpoint with the given payload.

        Parameters:
        - endpoint (str): The endpoint path to append to base URL.
        - payload: The JSON payload to include in the request body.

        Returns:
        - requests.models.Response: The response from the server.
        """
        return requests.post(
            self.url + endpoint,
            auth=self.authen_token,
            json=payload,
            timeout=20,
            verify=self.verify_ssl
        )

    def patch_request(self, endpoint: str, payload) -> requests.models.Response:
        """
        Sends a PATCH request to the specified endpoint with the given payload.

        Parameters:
        - endpoint (str): The endpoint path to append to base URL.
        - payload: The JSON payload to include in the request body.

        Returns:
        - requests.models.Response: The response from the server.
        """
        return requests.patch(
            self.url + endpoint,
            auth=self.authen_token,
            json=payload,
            timeout=20,
            verify=self.verify_ssl
        )

    def delete_request(self, endpoint: str, payload) -> requests.models.Response:
        """
        Sends a DELETE request to the specified endpoint with the given payload.

        Parameters:
        - endpoint (str): The endpoint path to append to base URL.
        - payload: The JSON payload to include in the request body.

        Returns:
        - requests.models.Response: The response from the server.
        """
        return requests.delete(
            self.url + endpoint,
            auth=self.authen_token,
            json=payload,
            timeout=20,
            verify=self.verify_ssl
        )
