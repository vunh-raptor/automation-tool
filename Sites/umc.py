from Common.page_object import page_object as Page
import logging


# Element Path
class umc(Page):
    # Base URL
    umc_url = "https://um.pdcvn1.vn.prod/user-management/spa/account/search?0"

    # Log in/Log out Path
    ldap_user_input = '//*[@id="IDToken1"]'
    ldap_pw_input = '//*[@id="IDToken2"]'
    login_button = '//*[@id="kc-login"]'
    logout_button = '//*[contains(text(),"Logout")]'

    # Elements in Searchs
    hrid_input = '//*[@id="id2"]'
    hrid_search_button = '//*[@id="id4"]'
    detail_button = '//*[contains(text(),"Detail")]'
    block_button = '//button//*[contains(text(),"Block")]'
    deactivate_button = '//button//*[contains(text(),"Deactivate")]'
    edit_button = '//button//*[contains(text(),"Edit")]'

    # Elements in Details
    available_select = '//select[contains(@name,"available")]'
    selected_select = '//select[contains(@name,"selected")]'
    arrow_button = '//button[contains(@class,"add")]'

    role_palette = '//*[@data-better-uid="role-palette"]'

    homesis_suffix = '//option[@value="HOMESIS"]'
    homesis_user_suffix = '//option[@value="HOMESIS_USER"]'

    # Save buttons
    save_button = '//button[contains(text(),"Save")]'

    # Function
    def get_umc_url(self) -> None:
        self.get(self.umc_url)

    def login_with_data(self, ldap_user: str, ldap_pw: str) -> bool:
        if (ldap_user is not None) & (ldap_pw is not None):
            self.search_by_xpath(self.ldap_user_input, delay=0.5).send_keys(ldap_user)
            self.search_by_xpath(self.ldap_pw_input, delay=0.5).send_keys(ldap_pw)
            return self.search_by_xpath(self.login_button, delay=0.5).click()
        else:
            logging.critical("Cannot ")

    def logout(self) -> None:
        self.search_by_xpath(self.logout_button).click()

    def search_hrid(self, hrid: str) -> None:
        self.search_by_xpath(self.hrid_input).send_keys(hrid)
        self.search_by_xpath(self.hrid_search_button).click()

    def click_details_button(self) -> None:
        self.search_by_xpath(self.detail_button).click()

    def click_block_button(self) -> bool:
        button = self.search_by_xpath(self.block_button)
        if button.flag:
            self.get_umc_url()
            return False
        else:
            button.click()
            return True

    def click_activate(self) -> bool:
        button = self.search_by_xpath(self.deactivate_button)
        if button.flag:
            self.get_umc_url()
            return False
        else:
            button.click()
            return True

    def click_edit(self) -> None:
        self.search_by_xpath(self.edit_button).click()

    def add_homesis(self) -> None:
        homesis = self.search_by_xpath(
            self.role_palette + self.available_select + self.homesis_suffix
        )
        if homesis.flag:
            homesis.click()
            self.search_by_xpath(self.role_palette + self.arrow_button).click()
            return True

        return False

    def add_homesis_user(self) -> None:
        homesis_user = self.search_by_xpath(
            self.role_palette + self.available_select + self.homesis_user_suffix
        )
        if homesis_user.flag:
            homesis_user.click()
            self.search_by_xpath(self.role_palette + self.arrow_button).click()
            return True

        return False

    def click_save(self) -> None:
        self.search_by_xpath(self.save_button).click()

    def search_activate_button(self) -> bool:
        deactivate = self.search_by_xpath(self.deactivate_button)
        return not deactivate.flag
