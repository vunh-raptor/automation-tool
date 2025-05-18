from Common.page_object import page_object as Page

# Element Path


class idm(Page):
    """This is a wrapper for IDM Page, based on the customed Page Object, which is also a wrapper of Selenium driver

    Args:
        Page (_type_): This is a wrapper for Selenium driver

    Returns:
        _type_: A customed BSL object
    """

    # Base URL
    idm_url = "https://idm.homecredit.vn/"

    # Login/Logout
    idm_login_button = '//*[@id="ext-gen31"]'

    # search
    idm_users_tab = '//*[@id="ext-gen23"]'
    idm_manage_user = '//*[@id="m-1"]'
    idm_view_user_extended = '//ul[@id="mp-1"]//li//a[@title="View User Extended"]'
    idm_view_user_modify = '//ul[@id="mp-1"]//li//a[@title="Modify User"]'
    idm_seacrh_user_dropdown_menu = '//*[@id="Filter.0.Field"]'
    idm_search_user_by_login_name_option = '//*[@id="Filter.0.Field"]//option[@value="idmLoginName02"]'
    idm_search_user_by_hr_code_option = '//*[@id="Filter.0.Field"]//option[@value="%USER_ID%"]'
    idm_input_search_value_field = '//*[@name="Filter.0.Value"]'
    idm_search_button = '//*[@id="imh_1"]'
    idm_search_button_in_modify_page = '//*[@id="imh_5"]'

    # user interaction
    idm_user_ratio_check = '//*[@id="listDisplayElement_0"]'
    idm_user_select_button = '//*[@id="ext-gen49"]'

    # user information
    idm_user_hr_code = '//*[@id="HCGDefaultUserSearch"]/tbody/tr[3]//td[2]'
    idm_user_login_name = '//*[@id="HCGDefaultUserSearch"]/tbody/tr[3]//td[3]'
    idm_user_organization = '//*[@id="HCGDefaultUserSearch"]/tbody/tr[3]//td[6]'
    idm_user_position = '//*[@id="HCGDefaultUserSearch"]/tbody/tr[3]//td[7]'
    idm_user_email = '//*[@id="HCGDefaultUserSearch"]/tbody/tr[3]//td[8]'
    idm_user_status = '//*[@id="HCGDefaultUserSearch"]/tbody/tr[3]//td[9]'

    # Function

    def get_idm_url(self) -> None:
        """
        This method navigates to the IDM URL.
        """
        self.get(self.idm_url)

    def click_login_button(self) -> bool:
        return self.search_by_xpath(self.idm_login_button, delay=0.5).click()

    def click_user_tab(self) -> bool:
        """this method click the user tab in IDM page

        Returns:
            bool: true if the user tab is clicked successfully, false otherwise
        """
        return self.search_by_xpath(self.idm_users_tab, delay=0.5).click()

    def click_manage_user(self) -> bool:
        """this method click the manage user option in IDM page

        Returns:
            bool: true if the manage user option is clicked successfully, false otherwise
        """
        return self.search_by_xpath(self.idm_manage_user, delay=0.5).click()

    def click_view_user_extended(self) -> bool:
        """This function is to click the view user extended tab

        Returns:
            bool: _description_
        """
        return self.search_by_xpath(self.idm_view_user_extended, delay=0.5).click()

    def click_view_user_modify(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return self.search_by_xpath(self.idm_view_user_modify, delay=1).click()

    def click_choose_search_user_type_of_info(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        if self.wait_element_to_visible(self.idm_search_button):
            return self.search_by_xpath(self.idm_seacrh_user_dropdown_menu).click()
        return False

    def choose_search_user_by_login_name_option(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return self.search_by_xpath(self.idm_search_user_by_login_name_option).click()

    def choose_search_user_by_hr_code_option(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return self.search_by_xpath(self.idm_search_user_by_hr_code_option).click()

    def input_search_value_field(self, idm_login_name) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        self.search_by_xpath(
            self.idm_input_search_value_field, delay=1).clearText()
        return self.search_by_xpath(self.idm_input_search_value_field, delay=0.5).send_keys(idm_login_name)

    def get_user_hr_code(self):
        return self.search_by_xpath(self.idm_user_hr_code, delay=0.5).get_value()

    def get_user_login_name(self):
        return self.search_by_xpath(self.idm_user_login_name, delay=0.5).get_value()

    def get_user_organization(self):
        return self.search_by_xpath(self.idm_user_organization, delay=0.5).get_value()

    def get_user_position(self):
        return self.search_by_xpath(self.idm_user_position, delay=0.5).get_value()

    def get_user_email(self):
        return self.search_by_xpath(self.idm_user_email, delay=0.5).get_value()

    def get_user_status(self):
        return self.search_by_xpath(self.idm_user_status, delay=0.5).get_value()

    def click_idm_search_button(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return self.search_by_xpath(self.idm_search_button, delay=0.5).click()

    def click_idm_search_button_in_modify_page(self) -> bool:
        return self.search_by_xpath(self.idm_search_button_in_modify_page, delay=0.5).click()

    # def click_check_ratio_user(self) -> bool:
    #     if self.wait_element_to_visible(self.idm_user_ratio_check):
    #         return self.search_by_xpath(self.idm_user_ratio_check, delay=0.5).click()
    #     return False

    def click_user_select_button(self) -> bool:
        return self.search_by_xpath(self.idm_user_select_button, delay=0.5).click()
