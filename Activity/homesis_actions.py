import time
from Sites.homesis import homesis
from Common.constant.error_message import ErrorMessage


def login_to_site(ldap_user: str, ldap_pw: str) -> homesis:
    """This is a funciton to login to Homesis with the provided username and password

    Args:
        ldap_user (str): username for LDAP
        ldap_pw (str): password for LDAP

    Returns:
        homesis: a object represent the Homesis Page in Selenium
    """
    homesis_page = homesis()
    homesis_page.get_homesis_url()
    homesis_page.login_with_data(ldap_user=ldap_user, ldap_pw=ldap_pw)
    return homesis_page


# This funtion is to add role in bank for SA
def add_role_in_bank_SA(homesis_page: homesis, hr_code: str, id_number: str, note: str, supervisor_code: str, role: str, location: str) -> list:
    """This function will add role in bank SA for users based on the given list

    Args:
        homesis_page (homesis): the object represent the Homesis Page in Selenium
        hr_code (str): hr code of user, take from given excel file
        id_number (str): id number of user, take from given excel file
        note (str): note for user, take from given excel file
        supervisor_code (str): supervisor code of user, take from given excel file
        role (str): role of user, take from given excel file
        location (str): location of user, take from given excel file

    Returns:
        list: this list contain a success/error messages of the action grant role in bank for user.
    """
    list_of_error = []
    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():
        if homesis_page.fill_id_number(id_number) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ID_NUMBER)
        if homesis_page.fill_role_in_bank(role) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ROLE)
        if homesis_page.fill_note(note) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_NOTE)
        if homesis_page.select_location(location):
            homesis_page.click_add_location()
            time.sleep(1)
            homesis_page.click_add_assign_district()
            time.sleep(1)
        else:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FIND_LOCATION)
        if homesis_page.chose_supervisor(supervisor_code) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FIND_SUP_CODE)
        if homesis_page.click_save_button():
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CLICK_SAVE_BUTTON)
    else:
        list_of_error.append(
            hr_code + "-" + ErrorMessage.homesis_message.CAN_NOT_FIND_USER)
    return list_of_error

# This funtion is to add role in bank for RA MW


def add_role_in_bank_RA_MW(homesis_page: homesis, hr_code: str, note: str, role: str) -> list:
    """This function will add role in bank RA MW for users based on the given list

    Args:
        homesis_page (homesis): the object represent the Homesis Page in Selenium
        hr_code (str): hr code of user, take from given excel file
        note (str): note for user, take from given excel file
        role (str): role of user, take from given excel file

    Returns:
        list: this list contain a success/error messages of the action grant role in bank for user.
    """
    list_of_error = []
    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():
        if homesis_page.fill_role_in_bank(role) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ROLE)
        if homesis_page.fill_note(note) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_NOTE)
        if homesis_page.click_save_button():
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CLICK_SAVE_BUTTON)
    else:
        list_of_error.append(
            hr_code + "-" + ErrorMessage.homesis_message.CAN_NOT_FIND_USER)
    return list_of_error

# This funtion is to add role in bank for RA FPT


def add_role_in_bank_RA_FPT(homesis_page: homesis, hr_code: str, note: str, id_number: str, role: str) -> list:
    """This function will add role in bank RA FPT for users based on the given list

    Args:
        homesis_page (homesis): the object represent the Homesis Page in Selenium
        hr_code (str): hr code of user, take from given excel file
        id_number (str): id number of user, take from given excel file
        note (str): note for user, take from given excel file       
        role (str): role of user, take from given excel file

    Returns:
        list: this list contain a success/error messages of the action grant role in bank for user.
    """

    list_of_error = []
    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():
        if homesis_page.fill_role_in_bank(role) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ROLE)
        if homesis_page.fill_id_number(id_number) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ID_NUMBER)
        if homesis_page.fill_note(note) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_NOTE)
        if homesis_page.click_save_button():
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CLICK_SAVE_BUTTON)
    else:
        list_of_error.append(
            hr_code + "-" + ErrorMessage.homesis_message.CAN_NOT_FIND_USER)
    return list_of_error

# This funtion is to add role in bank for RA New Segment


def add_role_in_bank_RA_New_Segment(homesis_page: homesis, hr_code: str, note: str, id_number: str, role: str, supervisor_code: str) -> list:
    """This function will add role in bank RA Newsegment for users based on the given list

    Args:
        homesis_page (homesis): the object represent the Homesis Page in Selenium
        hr_code (str): hr code of user, take from given excel file
        note (str): note for user, take from given excel file 
        id_number (str): id number of user, take from given excel file
        role (str): role of user, take from given excel file
        supervisor_code (str): supervisor code of user, take from given excel file

    Returns:
        list:  this list contain a success/error messages of the action grant role in bank for user
    """

    list_of_error = []
    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():
        if homesis_page.fill_id_number(id_number) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ID_NUMBER)
        if homesis_page.fill_role_in_bank(role) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ROLE)
        if homesis_page.fill_note(note) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_NOTE)
        if homesis_page.chose_supervisor(supervisor_code) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FIND_SUP_CODE)
        if homesis_page.click_save_button():
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CLICK_SAVE_BUTTON)
    return list_of_error

# This funtion is to change role in bank


def change_role_in_bank(homesis_page: homesis, hr_code: str, role: str) -> bool:
    """This function is to change role in bank for users

    Args:
        homesis_page (homesis): the object represent the Homesis Page in Selenium
        hr_code (str): hr code of user, take from given excel file
        role (str): role of user, take value form select-box on UI

    Returns:
        bool: true mean is has click save buton successfully
    """

    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():
        homesis_page.fill_role_in_bank("** choose **")
        time.sleep(2)
        homesis_page.fill_role_in_bank(role)
        time.sleep(2)
        return homesis_page.click_save_button()


# This funtion is to add sup code
def add_sup_code(homesis_page: homesis, hr_code: str, supervisor_code: str) -> list:
    """Function to add supervisor code for user

    Args:
        homesis_page (homesis): the object represent the Homesis Page in Selenium
        hr_code (str): hr code of user, take from given excel file
        supervisor_code (str): supervisor code of user, take from given excel file

    Returns:
        list:  this list contain a success/error messages of the action add sup code for user
    """

    list_of_error = []
    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():
        if homesis_page.chose_supervisor(supervisor_code) is False:
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FIND_SUP_CODE)
        if homesis_page.click_save_button():
            list_of_error.append(
                hr_code + " - " + ErrorMessage.homesis_message.CLICK_SAVE_BUTTON)
    else:
        list_of_error.append(
            hr_code + "-" + ErrorMessage.homesis_message.CAN_NOT_FIND_USER)
    return list_of_error

# This funtion is to update note


def update_note(homesis_page: homesis, hr_code: str, note: str) -> bool:
    """This function will clear the current note and update with a new note

    Args:
        homesis_page (homesis):  the object represent the Homesis Page in Selenium
        hr_code (str): hr code of user, take from given excel file
        note (str): note need to update for user, take from given excel file

    Returns:
        bool: true mean is has click save buton successfully
    """
    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():
        homesis_page.update_note(note)
        return homesis_page.click_save_button()

    return False

# This funtion is to update ID number


def update_id_number(homesis_page: homesis, hr_code: str, id_number: str) -> bool:
    """This function will clear the current ID number and update with a new ID number

    Args:
        homesis_page (homesis): the object represent the Homesis Page in Selenium
        hr_code (str): hr code of user, take from given excel file
        id_number (str): id number of user, take from given excel file

    Returns:
        bool: true mean is has click save buton successfully
    """
    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():
        homesis_page.update_id_number(id_number)
        return homesis_page.click_save_button()

# this fuction is to closed shopcode on homesis


def closed_partner(homesis_page: homesis, partner_code: str) -> bool:
    """_summary_

    Args:
        homesis_page (homesis): _description_
        partner_code (str): _description_

    Returns:
        bool: _description_
    """
    homesis_page.search_sales_code(sales_code=partner_code)

    if homesis_page.click_specific_info_sales_button():
        return homesis_page.click_on_closed_button()
