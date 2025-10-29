import logging
import time
from Common.page_object import page_object as Page
from Common.constant import app_logic_exception

# Element Path


class bsl(Page):
    """This is a wrapper for BSL Page, based on the customed Page Object, which is also a wrapper of Selenium driver

    Args:
        Page (_type_): This is a wrapper for Selenium driver

    Returns:
        _type_: A customed BSL object    
    """

    # Base URL
    bsl_url = "https://bsl.pdcvn1.vn.prod/bsl"

    # Login/Logout
    ldap_user_input = '//*[@id="username"]'
    ldap_pw_input = '//*[@id="password"]'
    login_button = '//*[@id="kc-login"]'
    logout_button = '//*[contains(text(),"Logout")]'  # Need update

    # Landing Xpath
    find_bank_branch_button = '//div[contains(text(), "Find bank branch")]'
    find_bank_url = 'https://bsl.pdcvn1.vn.prod/bsl/bank-search'

    # Find bank Xpath
    bank_name_input = '//*[@data-uid="name"]'
    bank_code_input = '//*[@data-uid="code"]'
    search_button = '//*[@name="buttonPanel:search"]'
    reset_button = '//*[@name="buttonPanel:reset"]'

    # bank detail Xpath
    new_branch_button = '//*[contains(@data-better-uid, "bank-branch-create-link")]'

    # Table xpath
    first_search_result = '//*[contains(@id, "first-row")]/following-sibling::tr[1]//td[1]//div'
    first_search_detail_button = '//*[contains(@id, "first-row")]/following-sibling::tr[1]//td[4]//div'

    # Create branch Xpath
    bank_branch_name = '//*[@data-uid="name"]'
    bank_branch_status = '//*[@data-uid="status"]'
    bank_branch_region = '//*[@data-uid="address.region-code"]'
    bank_branch_district = '//*[@data-uid="address.district-code"]'
    bank_branch_code = '//*[@data-uid="code"]'
    OK_button = '//*[@data-uid="button-panel:ok"]'

    # Function
    def get_bsl_url(self) -> None:
        """
        This method navigates to the UMC URL.
        """
        self.get(self.bsl_url)

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
                                 delay=1.0).send_keys(ldap_user)
            self.search_by_xpath(self.ldap_pw_input,
                                 delay=1.0).send_keys(ldap_pw)
            self.search_by_xpath(self.login_button, delay=1.0).click()
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

    def logout(self) -> None:
        """
        This method logs out of the current session.
        """
        # self.search_by_xpath(self.logout_button).click()
        pass

    def click_find_bank(self) -> None:
        """
        This method click find bank button on Homepage
        """
        self.get(self.find_bank_url)

    def click_find_bankbranch(self) -> None:
        """
        This method click find bank branch button on Homepage
        """
        self.search_by_xpath(self.find_bank_branch_button)

    def search_bank_name(self, bankname: str) -> None:
        """
        This method trigger search and return result for bank name searching
        """
        self.search_by_xpath(self.bank_name_input, delay=1.0).clearText()
        self.search_by_xpath(self.bank_name_input,
                             delay=1.0).send_keys(bankname)
        self.search_by_xpath(self.search_button, delay=1.0).click()

    def click_bank_detail(self) -> bool:
        """This is click bank detail method

        Returns:
            bool: The result if the button can be clicked or not
        """
        return self.search_by_xpath(self.first_search_detail_button, delay=1.0).click()

    def click_create_branch(self) -> bool:
        """This is click new branch button method

        Returns:
            bool: The result if the button can be clicked or not
        """
        return self.search_by_xpath(self.new_branch_button).click()

    def fill_branch_name(self, branch_name: str) -> bool:
        """This is fill bank branch name in create screen

        Returns:
            bool: _description_
        """
        return self.search_by_xpath(self.bank_branch_name, delay=2).send_keys(branch_name)

    def select_branch_status(self, value: str) -> None:
        """This is select branch staus in create screen

        Args:
            status (str): intended status to select that visible in the drop down box

        Returns:
            bool: 
        """
        return self.select_dropdown_value(self.bank_branch_status, value=value, delay=2)

    def fill_branch_code(self, code: str) -> bool:
        """This is to fill bank branch code in create screen

        Args:
            code (str): the branch code intended to be filled

        Returns:
            bool: result of the action
        """
        return self.search_by_xpath(self.bank_branch_code, delay=2).send_keys(code)

    def select_branch_region(self, region: str) -> None:
        """This is to select branch region

        Args:
            region (str): str value of branch region

        Returns:
            bool: result of the action
        """
        return self.select_dropdown_by_visible_text(self.bank_branch_region, value=region.strip(), delay=2)

    def select_branch_district(self, district: str) -> None:
        """This is to select branch district location, note that there is another data cleaning function to ensure the dropdown value can be selected on PROD env

        Args:
            district (str): str value of district

        Returns:
            bool: result of the action
        """
        # district = self.remove_district_prefix(
        #     district)  # cleaning function called
        return self.select_dropdown_by_contains_text(self.bank_branch_district, value=district, delay=2)

    def click_OK_create_button(self) -> bool:
        """This method finalize the bank branch creation with OK button
        """
        return self.search_by_xpath(self.OK_button).click()

    # def remove_district_prefix(self, district: str) -> str:
    #     """As the district information is always input manually, so there is no validation or alignment of data consistency.
    #     This function will perform trying to CLEAN the inputted data as much as it can

    #     Args:
    #         district (str): str value of district

    #     Returns:
    #         str: str value of district (after cleaning)
    #     """
    #     clean_data = ""
    #     lst = ['H.', 'Q.', 'TT.', 'TX.', 'TP.', 'Quận',
    #            'Huyện', 'Thị Xã', 'Thị Trấn', 'Thành Phố']
    #     for pref in lst:
    #         if pref in district:
    #             clean_data = district.replace(pref, '')
    #             return clean_data.strip()
    #     return district.strip()
