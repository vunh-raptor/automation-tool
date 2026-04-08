from Common.request_object import Session
from Common.supporting import filter_UMC_json_single_element
from string import Template
import json


class umc_request(Session):
    """A class representing a UMC session

    Args:
        Session (_type_): A session to use UMC request
    """

    # DEFAULT cURL for UMC Swagger API
    UMC_DEFAULT_URL = "https://um.pdcvn1.vn.prod/"
    _API_USER_MANAGEMENT = "api/accounts"
    _API_SCIM_USER_MANAGEMENT = "api/scim/Users/"
    _USER_MANAGEMENT = "user-management/"
    _API_SCIM_GROUP_MANAGEMENT = "api/scim/Groups/"

    # PARAMs for UMC Request API
    _EMPLOYEE_NUMBER_PARAM = "employeeNumber={param}"
    _UID_PARAM = "uid={param}"

    # Body Template for UMC Request API
    _PATCH_SINGLE_PARAM_BODY = Template("""
                                        {
                                            "${param}":${value}
                                            }""")

    # API body to patch roles
    _PATCH_ROLE_INFO = Template(
        """
        {
            "operation":"${action}",
            "value": "${login}"
        }
        """)
    _PATCH_MODIFY_ROLE_SKELETON = Template(
        """
        {
        "members": [
            ${value}
        ]
        }
        """
    )

    # API Body to patch phone numbers
    _PATCH_PHONE_PARAM_BODY = Template(
        """
        "phoneNumbers": [
            {
            "display": "${value}",
            "primary": "false",
            "type": "mobile",
            "value": "${value}"
            },
            {
            "display": "${value}",
            "primary": "true",
            "type": "work",
            "value": "${value}"
            }
        ]
        """
    )
    # API Body to patch email
    _PATCH_EMAIL_PARAM_BODY = Template(
        """
        "emails": [
            {
            "display": "${value}",
            "primary": "true",
            "type": "work",
            "value": "${value}"
            }
        ]
        """
    )

    # API Body to create new account
    _POST_NEW_ACCOUNT_BODY = Template(
        """
        {
        "active": true,
        "displayName": "${displayName}",
        "emails": [
            {
            "primary": true,
            "type": "work",
            "value": "${email}"
            }
        ],
        "externalId": "${hrcode}",
        "managedExternally": false,
        "name": {
            "familyName": "${lastName}",
            "givenName": "${firstName}"
        },
        "phoneNumbers": [
            {
            "primary": false,
            "type": "mobile",
            "value": "${phone}"
            },
            {
            "primary": true,
            "type": "work",
            "value": "${phone}"
            }
        ],
        "schemas": [
            "urn:scim:schemas:core:1.0"
        ],
        "startDate": "${startDate}",
        "title": "RA",
        "userName": "${login}"
        }
        """
        # Format startDate dd.mm.yy
    )

    def __init__(self, token: str, url: str = UMC_DEFAULT_URL, auth_type: str = "basic"):
        super().__init__(token, url, auth_type)

    def get_user_info_with_hrcode(self, hr_code: str, element: str) -> str:
        """send GET request to retrieve user info on UMC with hrcode placeholder

        Args:
            hr_code (str): hr code of the target account
            element (str): information that the request need to get

        Returns:
            dict: result of the account + element info - type DICT
        """
        endpoint = f"{self._USER_MANAGEMENT}{self._API_USER_MANAGEMENT}?{self._EMPLOYEE_NUMBER_PARAM.format(param=hr_code)}"
        response = self.get_request(endpoint=endpoint)
        return filter_UMC_json_single_element(response=response, element=element)

    def get_user_info_with_username(self, username: str, element: str) -> str:
        """send GET request to retrieve user info on UMC with username placeholder

        Args:
            username (str): _description_
            element (str): _description_

        Returns:
            str: _description_
        """
        endpoint = f"{self._USER_MANAGEMENT}{self._API_USER_MANAGEMENT}?{self._UID_PARAM.format(param=username)}"
        response = self.get_request(endpoint=endpoint)
        return filter_UMC_json_single_element(response=response, element=element)

    def patch_user_single_info(self, hr_code: str, element: str, value) -> bool:
        """send PATCH request to update user info on UMC

        Args:
            hr_code (str): HR code of the target account
            element (str): information that the request need to update

        Returns:
            bool: status of the request call
        """
        endpoint = f"{self._USER_MANAGEMENT}{self._API_SCIM_USER_MANAGEMENT}{hr_code}"
        payload = ""
        # Prepare payload based on element to update
        match element:
            case "phone":
                payload = json.loads(
                    self._PATCH_PHONE_PARAM_BODY.substitute(value=value))
            case "email":
                payload = json.loads(
                    self._PATCH_EMAIL_PARAM_BODY.substitute(value=value))
            case _:  # Default Case
                # Prepare JSON-safe value for template
                if isinstance(value, str):
                    value_json = f'"{value}"'  # Add quotes for strings
                elif isinstance(value, bool):
                    value_json = "true" if value else "false"  # Lowercase for JSON
                else:
                    value_json = value  # Numbers stay as-i

                payload = json.loads(self._PATCH_SINGLE_PARAM_BODY.substitute(
                    param=element, value=value_json))

        response = self.patch_request(endpoint=endpoint, payload=payload)
        # Verify the status of the request call
        if response.status_code >= 400:
            return False
        else:
            return True

    def patch_user_single_role(self, hr_codes: list, role: str, action: str) -> bool:
        """send PATCH request to update user role on UMC

        Args:
            hr_codes (list): list of HR code of the target accounts
            role (str): the role that need to take action
            action (str): the action that the PATCH will send (add / delete)

        Returns:
            bool: status of the request call
        """
        endpoint = f"{self._USER_MANAGEMENT}{self._API_SCIM_GROUP_MANAGEMENT}{role}"
        json_data = ""
        for code in hr_codes:
            json_data = json_data + \
                self._PATCH_ROLE_INFO.substitute(
                    action=action, login=code) + ",\n"
        json_data = json_data.rstrip(',\n')
        payload = json.loads(
            self._PATCH_MODIFY_ROLE_SKELETON.substitute(value=json_data))
        response = self.patch_request(endpoint=endpoint, payload=payload)

        # Verify the status of the request call
        if response.status_code >= 400:
            return False
        else:
            return True

    def patch_user_firstname_lastname(self, hr_code: str, first_name: str, last_name: str) -> bool:
        """send PATCH request to update user name on UMC

        Args:
            hr_code (str): hr code of the target account
            first_name (str): first name that needs to be updated
            last_name (str): last name that needs to be updated

        Returns:
            bool: status of the request
        """
        endpoint = f"{self._USER_MANAGEMENT}{self._API_SCIM_USER_MANAGEMENT}{hr_code}"
        payload = {
            "name": {
                "givenName": first_name,
                "familyName": last_name
            }
        }
        response = self.patch_request(endpoint=endpoint, payload=payload)
        print(response.content)
        # Verify the status of the request call
        if response.status_code >= 400:
            return False
        else:
            return True

    def create_new_account(self, new_accounts_data: dict) -> bool:
        """This is create new account request

        Args:
            new_accounts_data (dict): dictionary of data that the creating account contains

        Returns:
            bool: status of the action
        """
        endpoint = f"{self._USER_MANAGEMENT}{self._API_SCIM_USER_MANAGEMENT}"
        payload = json.loads(self._POST_NEW_ACCOUNT_BODY.substitute(
            hr_code=hr_code, displayName=displayName, email=email, lastName=lastName, firstName=firstName, phone=phone, startDate=startDate, login=login))
        response = self.post_request(endpoint=endpoint, payload=payload, )

        if response.status_code >= 400:
            return False
        else:
            return True

    def get_account_deactivation_date(self, hr_code: str) -> str:
        """This function is to get account deactivation date

        Args:
            hr_code (str): hr code of the account

        Returns:
            str: deactivation date of the account
        """
        endpoint = f"{self._USER_MANAGEMENT}{self._API_USER_MANAGEMENT}?{self._EMPLOYEE_NUMBER_PARAM.format(param=hr_code)}"
        response = self.get_request(endpoint=endpoint)
        return f"Deactivation Time: {filter_UMC_json_single_element(response=response, element='lastDeactivationTime').split('T')[0]}"
