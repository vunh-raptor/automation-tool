from Common.request_object import Session


class homesis_request(Session):
    """A class representing a Homesis session

    Args:
        Session (_type_): A session to use Homesis request
    """

    # Default cURL for Homesis Swagger API
    HOMESIS_DEFAULT_URL = "https://homesis.homecredit.vn/"
    _HOMESIS_MANAGEMENT = "homesis/"
    _API_USER_MANAGEMENT = "restful/users"
    _SUPERVISOR_MANAGEMENT = "subordinates"
    # Params for Homesis Swagger API
    _CODE_PARAM = "code={param}"

    def __init__(self, token: str, url: str = HOMESIS_DEFAULT_URL, auth_type: str = "basic"):
        super().__init__(token, url, auth_type)

    def get_user_info(self, hr_code: str, element: str) -> bool:
        """send GET request to retrieve user info on Homesis

        Args:
            hr_code (str): hr code of the target account
            element (str): information that the request need to get

        Returns:
            str: result of the account based element info - type str
        """
        endpoint = f"{self._HOMESIS_MANAGEMENT}{self._API_USER_MANAGEMENT}?{self._CODE_PARAM.format(param=hr_code)}"
        response = self.get_request(endpoint=endpoint)

        if response.status_code >= 400:
            return False
        else:
            print(response.text)
            return True

    def manage_supervisor(self, hr_code: str, supervisor_code: str, action: str = "assign"):
        """send POST/DELETE/GET request to assign/remove/retrieve Supervisor subordinates.

        Args:
            hr_code (str): hr code of target account (ignored for action="get")
            supervisor_code (str): the supervisor HR code
            action (str): "assign" | "delete" | "get"

        Returns:
            bool: True/False for assign and remove actions.
            Response: raw requests.Response for the get action so callers can parse the body.
        """
        endpoint = f"{self._HOMESIS_MANAGEMENT}{self._API_USER_MANAGEMENT}/{supervisor_code}/{self._SUPERVISOR_MANAGEMENT}"
        if action.strip().lower() == "assign":
            response = self.post_request(
                endpoint=endpoint, payload=[hr_code])
        elif action.strip().lower() == "delete":
            response = self.delete_request(
                endpoint=endpoint, payload=[hr_code])
        elif action.strip().lower() == "get":
            response = self.get_request(endpoint=endpoint)
            return response
        else:
            raise ValueError(
                f"Unsupported action for manage_supervisor: {action}")

        if response.status_code >= 400:
            print(response.text)
            return False
        else:
            print(response.text)
            return True