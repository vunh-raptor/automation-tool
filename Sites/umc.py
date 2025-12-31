import logging
import time
from Common.page_object import page_object as Page
from Common.constant import app_logic_exception
from Common.request_object import Session
from Common.supporting import filter_UMC_json_single_element
from string import Template
import json

# Element Path


class umc(Page):
    """This is a wrapper for UMC Page, based on the customed Page Object, which is also a wrapper of Selenium driver

    Args:
        Page (_type_): This is a wrapper for Selenium driver

    Returns:
        _type_: A customed UMC object
    """
    # Base URL
    umc_url = "https://um.pdcvn1.vn.prod/user-management/spa/account/search?0"

    # Log in/Log out Path
    ldap_user_input = '//*[@id="username"]'
    ldap_pw_input = '//*[@id="password"]'
    login_button = '//*[@id="kc-login"]'
    logout_button = '//*[contains(text(),"Logout")]'

    # Elements in Searchs
    hrid_input = '//*[@id="id2"]'
    hrid_search_button = '//*[@id="id4"]'
    detail_button = '//*[contains(text(),"Detail")]'
    block_button = '//button//*[contains(text(),"Block")]'
    deactivate_button = '//button//*[contains(text(),"Deactivate")]'
    activate_button = '//button//*[contains(text(),"Activate")]'
    edit_button = '//button//*[contains(text(),"Edit")]'
    search_result_status = '//div[@data-better-uid="search-results:status"]'

    # Elements in Details
    available_select = '//select[contains(@name,"available")]'
    selected_select = '//select[contains(@name,"selected")]'
    add_role_button = '//button[contains(@class,"add")]'
    remove_role_button = '//button[contains(@class,"remove")]'
    account_status_field = '//div[@data-better-uid="status"]'
    detail_phone = '//*[@data-better-uid="detail.phone"]'
    detail_mobile = '//*[@data-better-uid="detail.mobile"]'
    first_name = '//*[@data-better-uid="detail.name"]'
    last_name = '//*[@data-better-uid="detail.surname"]'
    mail = '//*[@data-better-uid="detail.mail"]'
    date_of_birth = '//*[@data-better-uid="detail.date-of-birth"]'
    detail_gender = '//*[@data-better-uid="detail.gender"]'
    employedSince = '//*[@data-better-uid="detail.employed-since"]'
    roles_table = '//*[@id="roles"]/tbody[contains(text(), "")]'

    role_palette = '//*[@data-better-uid="role-palette"]'
    first_owned_role = '//*[@data-better-uid="role-palette:selected-field"]/option'

    owned_role_prefixed = '//*[@data-better-uid="role-palette:selected-field"]'
    role_palette_suffix = '//option[@value="replaced_text"]'

    feedback_panel = '//span[@data-better-uid="feedback:feedbackul:message"]'

    # Save buttons
    save_button = '//button[contains(text(),"Save")]'

    # Function
    def get_umc_url(self) -> None:
        """
        This method navigates to the UMC URL.
        """
        self.get(self.umc_url)
        time.sleep(1)

    def login_with_data(self, ldap_user: str, ldap_pw: str) -> bool:
        """
        This method logs in with the provided LDAP user and password.

        Args:
            ldap_user (str): The LDAP username.
            ldap_pw (str): The LDAP password.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        if (ldap_user is not None) & (ldap_pw is not None):
            self.search_by_xpath(self.ldap_user_input,
                                 delay=0.5).send_keys(ldap_user)
            self.search_by_xpath(self.ldap_pw_input,
                                 delay=0.5).send_keys(ldap_pw)
            # if self.wait_element_to_visible(self.login_button)
            self.search_by_xpath(self.login_button, delay=0.5).click()
            # wait for login
            time.sleep(2)
            if self.check_login_status() is False:
                logging.critical("Invalid Username or Password.")
                raise app_logic_exception.LoginError
                # return False
            else:
                return True
        else:
            logging.critical("Missing Username or Password.")
            raise app_logic_exception.LoginError
            # return False

    def stop(self) -> None:
        self.end_process()

    def logout(self) -> None:
        """
        This method logs out of the current session.
        """
        self.search_by_xpath(self.logout_button).click()

    def search_hrid(self, hrid: str) -> None:
        """
        This method searches for a given HRID.

        Args:
            hrid (str): The HRID to search for.
        """
        self.search_by_xpath(self.hrid_input).send_keys(hrid)
        self.search_by_xpath(self.hrid_search_button).click()

    def update_info(self, field: str, data: str) -> bool:
        """
        This method update information by field

        Args:
            field (str): the field needed to be updated
            data (str): the new data

        Returns:
            bool: status of the action
        """
        update_field = self.search_by_xpath(xpath=field)
        update_field.click()
        update_field.clearText()
        return update_field.send_keys(data)

    def click_details_button(self) -> None:
        """
        This method clicks the details button.
        """

        self.search_by_xpath(self.detail_button, delay=0.5).click()

    def click_block_button(self) -> bool:
        """
        This method clicks the block button.

        Returns:
            bool: False if the button is flagged, True otherwise.
        """
        button = self.search_by_xpath(self.block_button)
        if button.flag:
            self.get_umc_url()
            return False
        else:
            button.click()
            return True

    def click_deactivate(self) -> bool:
        """
        This method clicks the deactivate button.

        Returns:
            bool: False if the button is clicked, True otherwise.
        """
        button = self.search_by_xpath(self.deactivate_button)
        if button.flag:
            button.click()
            return False
        else:
            self.get_umc_url()
            return True

    def click_activate(self) -> bool:
        """This method clicks the activate button

        Returns:
            bool: status of the action
        """
        button = self.search_by_xpath(self.activate_button, delay=0.5)
        if button.flag:
            button.click()
            return False
        else:
            self.get_umc_url()
            return True

    def click_edit(self) -> None:
        """
        This method clicks the edit button.
        """
        self.search_by_xpath(self.edit_button, delay=0.5).click()

    def click_remove_role(self) -> None:
        """
        This method clicks the remove role button.
        """
        remove_role = self.role_palette + self.remove_role_button
        remove_button = self.search_by_xpath(remove_role)
        return remove_button.click()

    def click_add_role(self) -> bool:
        """
        This method clicks the add role button.
        """
        add_role = self.role_palette + self.add_role_button
        add_button = self.search_by_xpath(add_role, delay=0.5)
        return add_button.click()

    def is_table_is_empty(self) -> bool:
        """This method check the table is empty or not"""
        table = self.search_by_xpath(self.roles_table, delay=0.5)
        return table is not None

    def click_save(self) -> bool:
        """
        This method clicks the save button.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        return self.search_by_xpath(self.save_button).click()

    def search_activate_button(self) -> bool:
        """
        This method searches for the activate button.

        Returns:
            bool: False if the button is flagged, True otherwise.
        """
        deactivate = self.search_by_xpath(self.deactivate_button)
        return not deactivate.flag

    def get_details_account_status(self) -> str:
        """
        This method gets the details of the account status.

        Returns:
            str: The text of the status element.
        """
        status = self.search_by_xpath(self.account_status_field, delay=0.5)
        if status.flag:
            element = status.return_element()
            return element.text

    def get_search_account_status(self) -> str:
        """
        This method gets the search account status.

        Returns:
            str: The text of the status element.
        """
        status = self.search_by_xpath(self.search_result_status, delay=0.5)
        if status.flag:
            element = status.return_element()
            return element.text
        return "Account not found"

    def search_first_owned_role(self) -> bool:
        """
        This method searches for the first owned role.

        Returns:
            bool: True if the role is found, False otherwise.
        """
        role_selected_field = self.search_by_xpath(self.first_owned_role)
        return role_selected_field.flag

    def select_first_role(self) -> bool:
        """
        This method selects the first role.

        Returns:
            bool: True if the role is selected, False otherwise.
        """
        role_selected_field = self.search_by_xpath(self.first_owned_role)
        if role_selected_field.flag:
            role_selected_field.click()
            return True
        else:
            return False

    def verify_updated_info(self) -> bool:
        """
        This method verifies if the info is updated.

        Returns:
            bool: True if the role is updated, False otherwise.
        """
        updated_notif = self.search_by_xpath(self.feedback_panel)

        if updated_notif.flag:
            text = updated_notif.return_element().text
            return ("has been updated" in text)
        return False

    def select_role(self, role: str) -> bool:
        """
        This method selects a role.

        Args:
            role (str): The role to select.

        Returns:
            bool: True if the role is selected, False otherwise.
        """
        suffix = self.role_palette_suffix.replace("replaced_text", role)
        xpath = self.role_palette + suffix

        return self.search_by_xpath(xpath=xpath, delay=0.5).click()

    def select_owned_role(self, role: str) -> bool:
        """
        This method selects an owned role.

        Args:
            role (str): The role to select.

        Returns:
            bool: True if the role is selected, False otherwise.
        """
        role_suffix = self.role_palette_suffix.replace("replaced_text", role)
        xpath = self.owned_role_prefixed + role_suffix
        owned_role = self.search_by_xpath(xpath=xpath)
        return owned_role.click()


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
    # API Body to patch First name & last name
    _PATCH_NAME_PARAM_BODY = Template(
        """
        "name": {
            "familyName": "${lastName}",
            "givenName": "${firstName}"
        }
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

    def get_user_info(self, hr_code: str, element: str) -> str:
        """send GET request to retrieve user info on UMC

        Args:
            hr_code (str): hr code of the target account
            element (str): information that the request need to get

        Returns:
            dict: result of the account + element info - type DICT
        """
        endpoint = f"{self._USER_MANAGEMENT}{self._API_USER_MANAGEMENT}?{self._EMPLOYEE_NUMBER_PARAM.format(param=hr_code)}"
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
            case "firstname":
                payload = json.loads(
                    self._PATCH_NAME_PARAM_BODY.substitute(firstName=value))
            case "lastname":
                payload = json.loads(
                    self._PATCH_NAME_PARAM_BODY.substitute(lastName=value))
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
        # payload = json.loads(self._PATCH_MODIFY_ROLE_SINGLE_USER.substitute(
        #     action=action, login=hr_code))
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
        response = self.post_request(endpoint=endpoint, payload=payload)

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
