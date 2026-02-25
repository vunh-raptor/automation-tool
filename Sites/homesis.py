import logging
import time
from Common.page_object import page_object as Page
from selenium.common.exceptions import TimeoutException
from requests import Response
from Common.request_object import Session
from Common.constant import app_logic_exception

# Element Path


class homesis(Page):
    """This is a wrapper for homesis Page, based on the customed Page Object, which is also a wrapper of Selenium driver

    Args:
        Page (_type_): This is a wrapper for Selenium driver

    Returns:
        _type_: A customed HomeSis
    """

    # Base URL
    homesis_url = "https://homesis.homecredit.vn/homesis/"
    # homesis_url = "https://homesis.vn00c1.vn.infra/homesis/"

    # Swagger URL
    swagger_url = "https://homesis.vn.prod/homesis/restful/swagger-ui.html"
    # Non-prod link
    # homesis_url = "https://homesis.vn01p.vn.nonprod/homesis/"

    # Log in/Log out Path
    ldap_user_input = '//*[@id="username"]'
    ldap_pw_input = '//*[@id="password"]'
    login_button = '//*[@id="kc-login"]'

    # Homesis tab path
    homesis_tab_sale_admin = '//table[@onmouseover = "showTooltip(\'Sales administration\');"]//a[@class = "abtn"]'
    homesis_tab_people_management = '//table[@onmouseover = "showTooltip(\'People management\');"]//a[@class = "abtn"]'
    homesis_tab_application_support = '//table[@onmouseover = "showTooltip(\'Application support\');"]//a[@class = "abtn"]'
    homesis_tab_user_management = '//*[@id="user"]//tbody//nobr'
    homesis_tab_admin_of_partner = '//*[@id="partner"]//tbody//nobr'

    # Elements in people management searchs
    hrid_input = '//*[@id="code"]'
    hrid_search_button = (
        '//table[@onmouseover = "showTooltip(\'Search users\');"]//a[@class = "abtn"]'
    )
    detail_button = "//a[@onmouseover = \"showSisTooltip('User information');\"]"
    search_result_status = "/html/body/table/tbody/tr[3]/td[2]/table/tbody/tr/td/div[6]/table/tbody/tr/td[10]"

    # Elements in sale admin searchs
    sales_code_input = '//*[@id="code"]'
    partner_code_search_button = '//table[@onmouseover = "showTooltip(\'Search a trade partner according to criteria\');"]//a[@class = "abtn"]'
    shop_code_search_button = '//table[@onmouseover = "showTooltip(\'Search salesroom\');"]//a[@class = "abtn"]'

    # Element in partner/shop information page
    partner_detailed_button = (
        "//a[@onmouseover = \"showSisTooltip('Detail of partner');\"]"
    )
    change_status_to_close_button = '//table[@onmouseover = "showTooltip(\'Immediately set status to Closed\');"]//a[@class = "abtn"]'
    change_status_to_block_button = '//table[@onmouseover = "showTooltip(\'Immediately set status to Blocked\');"]//a[@class = "abtn"]'
    partner_management_id_field = '//*[@id="partnerManagerId"]'
    contact_group_button = '//table[@onmouseover = "showTooltip(\'Show tab with list of actual assigned Cobrand groups\');"]//a[@class = "abtn"]'

    # Elements in edit user information page
    homesis_role_bank_selector = '//*[@id="userRole"]'
    homesis_id_number_text = '//*[@id="idCardNumber"]'
    homesis_note_text_field = '//*[@id="note"]'
    homesis_supervisors_tab = (
        '//table[@onmouseover = "showTooltip(\'Supervisors\');"]//a[@class = "abtn"]'
    )
    homesis_supervisors_data_tab = '//tr[@class="tdrow2"]'
    homesis_supervisor_choose_button = '//table[@onmouseover = "showTooltip(\'Attach supervisor\');"]//a[@class = "abtn"]'
    homesis_supervisors_code_text = '//*[@id="code"]'
    homesis_supervisors_search_btn = (
        '//table[@onmouseover = "showTooltip(\'Search users\');"]//a[@class = "abtn"]'
    )
    homesis_supervisors_checkbox = (
        '//table[@id= "septaTable"]//input[@name ="usersToAttach"]'
    )
    homesis_supervisors_attached_button = '//table[@onmouseover = "showTooltip(\'TT_USER_ATTACH_SELECTED\');"]//a[@class = "abtn"]'
    homesis_save_button = (
        '//table[@onmouseover = "showTooltip(\'Update user\');"]//a[@class = "abtn"]'
    )
    location_palette = '//*[@id="regdistricts"]'
    location_palette_suffix = '//option[@title="replaced_text"]'
    add_location_button = '//div[@id="#userSalesDistricts"]//a[text()="Add"]'
    assign_district_button = (
        '//div[@id="#userSalesDistricts"]//a[text()="Assign districts"]'
    )

    def get_homesis_url(self) -> None:
        """
        This method navigates to the homesis URL.
        """
        self.get(self.homesis_url)

    def get_homesis_swagger(self) -> None:
        """
        This method navigates to the swaggerUI API URL
        """
        self.get(self.swagger_url)

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

    def access_user_managerment(self) -> bool:
        """
        This method accesses the user management section of the application.

        Returns:
            bool: True if access is successful, False otherwise.
        """
        self.search_by_xpath(
            self.homesis_tab_people_management, delay=0.5).click()
        return self.search_by_xpath(self.homesis_tab_user_management, delay=0.5).click()

    def access_sales_managerment(self) -> bool:
        """
        This method accesses the sale management section of the application.

        Returns:
            bool: True if access is successful, False otherwise.
        """
        self.search_by_xpath(self.homesis_tab_sale_admin, delay=0.5).click()
        return self.search_by_xpath(
            self.homesis_tab_admin_of_partner, delay=0.5
        ).click()

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

    def click_details_button(self) -> bool:
        """
        This method clicks the details button.
        """
        return self.search_by_xpath(self.detail_button).click()

    def search_hrid(self, hrid: str) -> None:
        """
        This method searches for a given HRID.

        Args:
            hrid (str): The HRID to search for.
        """
        self.search_by_xpath(self.hrid_input, delay=0.5).clearText()
        self.search_by_xpath(self.hrid_input, delay=0.5).send_keys(hrid)
        self.search_by_xpath(self.hrid_search_button, delay=0.5).click()

    def search_sales_code(self, sales_code: str) -> None:
        """
        This method searches for a given partner/saleroom code.

        Args:
            sales_code (str): The partner/ salesroom code.
        """
        if self.wait_element_to_visible(self.partner_management_id_field) and (sales_code != ''):
            self.search_by_xpath(self.sales_code_input, delay=0.5).clearText()
            self.search_by_xpath(self.sales_code_input,
                                 delay=0.5).send_keys(sales_code)
            self.search_by_xpath(
                self.partner_code_search_button, delay=0.5).click()

    def click_specific_info_sales_button(self) -> bool:
        """Clicks the specific info sales button if it is visible.

        Args:
            detail_button (str): The XPath of the detail button.

        Returns:
            bool: True if the button was clicked, False otherwise.
        """
        if self.wait_element_to_visible(self.partner_detailed_button):
            self.search_by_xpath(self.partner_detailed_button).click()
            return True
        return False

    def fill_id_number(self, id_number) -> bool:
        """
        This method fills the ID number field.

        Args:
            id_number (str): The ID number to fill in.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            if self.wait_element_to_visible(self.homesis_id_number_text):
                self.search_by_xpath(self.homesis_id_number_text).clearText()
                self.search_by_xpath(
                    self.homesis_id_number_text).send_keys(id_number)
                return True
        except TimeoutException:
            print("Timeout while waiting for elements.")
        return False

    def fill_note(self, note) -> bool:
        """
        This method fills the note field.

        Args:
            note (str): The note to fill in.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            if self.wait_element_to_visible(self.homesis_note_text_field):
                self.search_by_xpath(
                    self.homesis_note_text_field).send_keys(note)
                return True
        except TimeoutException:
            print("Timeout while waiting for elements.")
        return False

    def update_note(self, note) -> bool:
        """
        This method updates the note field.

        Args:
            note (str): The note to update.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            if self.wait_element_to_visible(self.homesis_note_text_field):
                self.search_by_xpath(self.homesis_note_text_field).clearText()
                self.search_by_xpath(
                    self.homesis_note_text_field).send_keys(note)
                return True
        except TimeoutException:
            print("Timeout while waiting for elements.")
        return False

    def update_id_number(self, id_number) -> bool:
        """
        This method updates the Id number field field.

        Args:
            id_number (str): The Id number to update.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            if self.wait_element_to_visible(self.homesis_id_number_text):
                self.search_by_xpath(self.homesis_id_number_text).clearText()
                self.search_by_xpath(
                    self.homesis_id_number_text).send_keys(id_number)
                return True
        except TimeoutException:
            print("Timeout while waiting for elements.")
        return False

    def fill_role_in_bank(self, role) -> bool:
        """
        This method fills the role in bank field.

        Args:
            role (str): The role to fill in.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            if self.wait_element_to_visible(self.homesis_role_bank_selector):
                self.search_by_xpath(
                    self.homesis_role_bank_selector).send_keys(role)
                return True
        except TimeoutException:
            print("Timeout while waiting for elements.")
        return False

    def click_add_location(self) -> bool:
        """
        This method clicks the add location button.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        return self.search_by_xpath(self.add_location_button, delay=1).click()

    def click_add_assign_district(self) -> bool:
        """
        This method clicks the add assign district button.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            if self.wait_element_to_visible(self.assign_district_button):
                self.search_by_xpath(
                    self.assign_district_button).click()
                return True
        except TimeoutException:
            print("Timeout while waiting for elements.")
        return False

    def chose_supervisor(self, supervisor_code) -> bool:
        """
        This method chooses a supervisor.

        Args:
            supervisor_code (str): The supervisor code to choose.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        self.search_by_xpath(self.homesis_supervisors_tab, delay=0.5).click()
        if(self.search_by_xpath(self.homesis_supervisors_data_tab, delay=0.5).flag):
            return False
        self.search_by_xpath(
            self.homesis_supervisor_choose_button, delay=0.5).click()
        self.search_by_xpath(
            self.homesis_supervisors_attached_button, delay=0.5
        ).click()
        self.search_by_xpath(self.homesis_supervisors_code_text, delay=0.5).send_keys(
            supervisor_code
        )
        self.search_by_xpath(
            self.homesis_supervisors_search_btn, delay=0.5).click()
        self.search_by_xpath(
            self.homesis_supervisors_checkbox, delay=0.5).click()
        return self.search_by_xpath(
            self.homesis_supervisors_attached_button, delay=0.5
        ).click()

    def select_location(self, location: str) -> bool:
        """
        This method selects a location of SA.

        Args:
            location (str): The location to select.

        Returns:
            bool: True if the location is selected, False otherwise.
        """
        suffix = self.location_palette_suffix.replace(
            "replaced_text", location)
        xpath = self.location_palette + suffix
        return self.search_by_xpath(xpath=xpath, delay=0.5).click()

    def click_save_button(self) -> bool:
        """
        This method clicks the save button.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            if self.wait_element_to_visible(self.homesis_save_button):
                self.search_by_xpath(
                    self.homesis_save_button).click()
                return True
        except TimeoutException:
            print("Timeout while waiting for elements.")
        return False

    def click_on_closed_button(self) -> bool:
        """this function is click on the closed button in sale management section

        Returns:
            bool: true if the confirm alert is click ok successfully
        """
        try:
            if self.wait_element_to_visible(self.contact_group_button):
                if self.wait_element_to_visible(self.change_status_to_close_button):
                    self.search_by_xpath(
                        self.change_status_to_close_button).click()
                    self.accept_the_alert_pop_up()
                    return True
        except TimeoutException:
            print("Timeout while waiting for elements.")
        return False
# --------------------------------------------------------------------------------


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

    def __init__(self, token: str, url: str, auth_type: str = "basic"):
        super().__init__(token, url, auth_type)

    def get_user_info(self, hr_code: str, element: str) -> bool:
        """send GET request to retrieve user info on Homesis

        Args:
            hr_code (str): hr code of the target account
            element (str): information that the request need to get

        Returns:
            str: result of the account based element info - type str
        """
        endpoint = f"{self.HOMESIS_DEFAULT_URL}{self._HOMESIS_MANAGEMENT}{self._API_USER_MANAGEMENT}?{self._CODE_PARAM.format(param=hr_code)}"
        response = self.get_request(endpoint=endpoint)

        if response.status_code >= 400:
            return False
        else:
            print(response.text)
            return True

    def manage_supervisor(self, hr_code: str, supervisor_code: str, action: str = "assign") -> bool:
        """send POST/DELETE request to assign/remove Supervisor - affect to the user account

        Args:
            hr_code (str): hr code of target account
            supervisor_code (str): the supervisor code need to be added
            method (str): method to 

        Returns:
            bool: status of the request
        """
        endpoint = f"{self.HOMESIS_DEFAULT_URL}{self._HOMESIS_MANAGEMENT}{self._API_USER_MANAGEMENT}/{supervisor_code}/{self._SUPERVISOR_MANAGEMENT}"
        if action.strip().lower() == "assign":
            response = self.post_request(
                endpoint=endpoint, payload=[hr_code])
        elif action.strip().lower() == "remove":
            response = self.delete_request(
                endpoint=endpoint, payload=[hr_code])
        else:
            raise ValueError(
                f"Unsupported method to manage Supervisor: {action}")

        if response.status_code >= 400:
            return False
        else:
            print(response.text)
            return True
