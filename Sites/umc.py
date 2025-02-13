import logging
from Common.page_object import page_object as Page


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
    reactivate_button = '//button//*[contains(text(),"Activate")]'
    edit_button = '//button//*[contains(text(),"Edit")]'
    search_result_status = '//div[@data-better-uid="search-results:status"]'

    # Elements in Details
    available_select = '//select[contains(@name,"available")]'
    selected_select = '//select[contains(@name,"selected")]'
    add_role_button = '//button[contains(@class,"add")]'
    remove_role_button = '//button[contains(@class,"remove")]'
    account_status_field = '//div[@data-better-uid="status"]'

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
            self.search_by_xpath(self.ldap_user_input, delay=0.5).send_keys(ldap_user)
            self.search_by_xpath(self.ldap_pw_input, delay=0.5).send_keys(ldap_pw)
            return self.search_by_xpath(self.login_button, delay=0.5).click()
        else:
            logging.critical("Missing Username or Password.")
            return False

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

    def click_details_button(self) -> None:
        """
        This method clicks the details button.
        """
        self.search_by_xpath(self.detail_button).click()

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
       
    def click_edit(self) -> None:
        """
        This method clicks the edit button.
        """
        self.search_by_xpath(self.edit_button).click()

    def click_remove_role(self) -> None:
        """
        This method clicks the remove role button.
        """
        remove_role = self.role_palette + self.remove_role_button
        remove_button = self.search_by_xpath(remove_role)
        return remove_button.click()

    def click_add_role(self) -> None:
        """
        This method clicks the add role button.
        """
        add_role = self.role_palette + self.add_role_button
        add_button = self.search_by_xpath(add_role)
        return add_button.click()

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
            element = role_selected_field.click()
            return True
        else:
            return False

    def verify_updated_role(self) -> bool:
        """
        This method verifies if the role is updated.

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
        suffix = self.role_palette_suffix.replace("replaced_text",role)
        xpath = self.role_palette + suffix

        return self.search_by_xpath(xpath=xpath).click()

    def select_owned_role(self, role: str) -> bool:
        """
        This method selects an owned role.

        Args:
            role (str): The role to select.

        Returns:
            bool: True if the role is selected, False otherwise.
        """
        role_suffix = self.role_palette_suffix.replace("replaced_text",role)
        xpath = self.owned_role_prefixed + role_suffix
        owned_role = self.search_by_xpath(xpath=xpath)
        return owned_role.click()