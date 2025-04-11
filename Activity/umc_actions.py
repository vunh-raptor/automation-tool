from Sites.umc import umc
from Common.constant.error_message import ErrorMessage
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

roles_table = [
    "NON_HOSEL_USER",
    "SALES_AGENT_MISTAKE_30DAYS",
    "SALES_AGENT_HARD_TRIGGER",
    "SALES_AGENT_TEMP_DEACTIVE",
    "SALES_AGENT_AF_DEACTIVE",
]


def login_to_site(ldap_user: str, ldap_pw: str) -> umc:
    """This is a funciton to login to UMC with the provided username and password

    Args:
        ldap_user (str): username for UMC/LDAP
        ldap_pw (str): password for UMC/LDAP

    Returns:
        umc: a object represent the UMC Page in Selenium
    """
    umc_page = umc()
    umc_page.get_umc_url()
    umc_page.login_with_data(ldap_user=ldap_user, ldap_pw=ldap_pw)
    return umc_page


def add_homesis_homesis_user(umc_page: umc, hr_code: str) -> bool:
    """This is a function to active a user and adding HOMESIS and HOMESIS_USER as his owned roles

    Args:
        umc_page (umc): the object represent the UMC Page in Selenium
        hr_code (str): the HR Code being used

    Returns:
        bool: _description_
    """
    umc_page.search_hrid(hrid=hr_code)
    # Get account Status before running
    account_status = umc_page.get_search_account_status()

    # Check if account is Inactive
    if account_status != "Inactive":
        umc_page.click_details_button()
        umc_page.click_edit()

        # Add HOMESIS and HOMESIS_USER role
        umc_page.select_role(role="HOMESIS")
        umc_page.click_add_role()
        umc_page.select_role(role="HOMESIS_USER")
        umc_page.click_add_role()

        # Clicking Save
        umc_page.click_save()
    return umc_page.verify_updated_role()


def add_role_umc(umc_page: umc, login_name: str, role_list: list) -> bool:
    umc_page.search_hrid(hrid=login_name)
    # Get account Status before running
    account_status = umc_page.get_search_account_status()

    # Check if account is Inactive
    if account_status != "Inactive":
        umc_page.click_details_button()
        umc_page.click_edit()

        for index in range(len(role_list)):
            time.sleep(0.5)
            role = role_list[index]
            time.sleep(0.5)
            umc_page.select_role(role=role)
            time.sleep(0.5)
            umc_page.click_add_role()

        # Clicking Save
        umc_page.click_save()
    return umc_page.verify_updated_role()


def remove_role_umc(umc_page: umc, login_name: str, role_list: list) -> bool:
    umc_page.search_hrid(hrid=login_name)
    # Get account Status before running
    account_status = umc_page.get_search_account_status()

    # Check if account is Inactive
    if account_status != "Inactive":
        umc_page.click_details_button()
        umc_page.click_edit()

        for index, value in enumerate(role_list):
            time.sleep(0.5)
            role = role_list[index]
            time.sleep(0.5)
            umc_page.select_role(role=role)
            time.sleep(0.5)
            umc_page.click_remove_role()

        # Clicking Save
        umc_page.click_save()
    return umc_page.verify_updated_role()


def deactivate_user_with_reason(umc_page: umc, hr_code: str, reason: str) -> bool:
    """This is a funciton to clear user of all roles and add in only the dismissal role.

    Args:
        umc_page (umc): an object represnet the UMC page in Selenium
        hr_code (str): the HR Code we want to process
        reason (str): the dismissal roles of users

    Returns:
        bool: whether this run correctly or not
    """
    umc_page.search_hrid(hrid=hr_code)

    # Get account status beore running
    account_status = umc_page.get_search_account_status()

    # Check if account is Inactive
    if account_status != "Inactive":
        umc_page.click_details_button()
        umc_page.click_edit()

        # Check for existing dismissal roles

        dismissed = False
        for dismissal in roles_table:
            if umc_page.select_owned_role(role=dismissal):
                dismissed = True
                break

        # If user is not dismissed already, remove all roles
        if not dismissed:
            while umc_page.search_first_owned_role():
                umc_page.select_first_role()
                umc_page.click_remove_role()

        # Add Dismissal role
        umc_page.select_role(reason)
        umc_page.click_add_role()

        # Clicking Save
        umc_page.click_save()

        # Remove Successful or not. Return TRUE if Updated Successfully
        return umc_page.verify_updated_role()
    return False

def sales_reactivate(umc_page: umc, hr_code: str) -> bool:
    """This is a funciton to clear user of all dismissal roles and add in HOMESIS and HOMESIS_USER.

    Args:
        umc_page (umc): an object represnet the UMC page in Selenium
        hr_code (str): the HR Code we want to process
        reason (str): the dismissal roles of users

    Returns:
        bool: whether this run correctly or not
    """
    umc_page.search_hrid(hrid=hr_code)

    # Get account status beore running
    account_status = umc_page.get_search_account_status()

    # Check if account is Inactive
    if account_status != "Inactive":
        umc_page.click_details_button()
        umc_page.click_edit()

        # Check for existing dismissal roles

        for dismissal in roles_table:
            if umc_page.select_owned_role(role=dismissal):
                umc_page.click_remove_role()

        # Add Homesis and HOMESIS_USER role
        umc_page.select_role("HOMESIS")
        umc_page.click_add_role()

        # Clicking Save
        umc_page.click_save()

        # Remove Successful or not. Return TRUE if Updated Successfully
        return umc_page.verify_updated_role()

    return False

def remove_role(umc_page: umc, hr_code: str, role: str) -> bool:
    """
    Removes a specified role from a user in the UMC page.

    This function searches for a user by their HR code, checks if the account is active,
    and if so, removes the specified role from the user. The function then saves the changes
    and verifies if the role has been successfully removed.

    Args:
        umc_page (umc): The UMC page object where the operations are performed.
        hr_code (str): The HR code of the user.
        role (str): The role to be removed from the user.

    Returns:
        bool: True if the role was successfully removed, False otherwise.
    """

    umc_page.search_hrid(hrid=hr_code)
    # Get account Status before running
    account_status = umc_page.get_search_account_status()

    # Check if account is Inactive
    if account_status != "Inactive":
        umc_page.click_details_button()
        umc_page.click_edit()

        # Add HOMESIS and HOMESIS_USER role
        umc_page.select_role(role=role)
        umc_page.click_remove_role()

        # Clicking Save
        umc_page.click_save()

    return umc_page.verify_updated_role()


def deactivate_ra(umc_page: umc, hr_code: str) -> bool:
    """_Deactive a specific RA account in UMC page

    Args:
        umc_page (umc): The UMC page object where the operations are performed.
        hr_code (str): The HR code of the user.

    Returns:
        bool: True if successfully click the deactive button
    """
    umc_page.search_hrid(hrid=hr_code)
    # Get account Status before running
    account_status = umc_page.get_search_account_status()

    # Check if account is Inactive
    if account_status != "Inactive":
        umc_page.click_details_button()
    # Click deactive button
    return umc_page.click_deactivate()


def check_inactive(umc_page: umc, hr_code: str) -> str:
    """This function used to check if account is active or not

    Args:
        umc_page (umc): active UMC session
        hr_code (str): target HR code

    Returns:
        str: status result
    """
    
    umc_page.search_hrid(hrid=hr_code)
    # Get account Status before running
    account_status = umc_page.get_search_account_status()  # Store the status
    # if status == "Inactive":
    #     return "Inactive"
    # elif status == "Active":  # Use elif for efficiency
    #     return "Active"
    # elif status == "Account not found":
    #     return "Not Found"
    # else:
    #     return "Not Found"
    if account_status == "Account not found":
        return "Not found"
    return account_status

def update_phone_number(umc_page: umc, hr_code: str, phone_number: str) -> list:
    """_summary_

    Args:
        umc_page (umc): _description_
        hr_code (str): _description_
        phone_number (str): _description_

    Returns:
        list: _description_
    """
    
    list_of_error = []
    umc_page.search_hrid(hrid=hr_code)
    account_status = umc_page.get_search_account_status()
    # Get account Status before running
    # Check if account is Inactive
    if account_status == "Inactive":
        list_of_error.append(hr_code + " - " + ErrorMessage.umc_message.USER_INACTIVE)
    if account_status == "Account not found":
        list_of_error.append(hr_code + " - " + ErrorMessage.umc_message.USER_NOT_FOUND)
    if account_status == "Active":
        # Account found, start update phone actions
        umc_page.click_details_button()
        umc_page.click_edit()
        umc_page.update_phone(phone_number=phone_number)
        umc_page.click_save()
        # Check if Update successfully
        list_of_error.append(hr_code + " - " + ErrorMessage.umc_message.USER_UPDATED)
    return list_of_error

def update_name(umc_page: umc, hr_code: str, first_name: str, last_name: str) -> list:
    """_summary_

    Args:
        umc_page (umc): active umc session
        hr_code (str): _description_
        first_name (str): _description_
        last_name (str): _description_

    Returns:
        list(str): _description_
    """
    
    list_of_error = []
    umc_page.search_hrid(hrid=hr_code)
    # Get account Status before running
    account_status = umc_page.get_search_account_status()
    # Check if account is Inactive
    if account_status == "Inactive":
        list_of_error.append(hr_code + " - " + ErrorMessage.umc_message.USER_INACTIVE)
    if account_status == "Account not found":
        list_of_error.append(hr_code + " - " + ErrorMessage.umc_message.USER_NOT_FOUND)
    if account_status == "Active":
        # Account found, start update name actions
        umc_page.click_details_button()
        umc_page.click_edit()
        umc_page.update_name(first_name=first_name, last_name=last_name)
        umc_page.click_save()
        # Check if Update successfully
        list_of_error.append(hr_code + " - " + ErrorMessage.umc_message.USER_UPDATED)
    return list_of_error

def reactivate_account(umc_page: umc, hr_code: str) -> bool:
    """This function reactivate the target account. Ex: Deactivated -> Activate

    Args:
        umc_page (umc): active umc session
        hr_code (str): the target account/hr code
    """
    umc_page.search_hrid(hrid=hr_code)
    if umc_page.get_search_account_status() == "Inactive":
        # Account is found and not in Inactive status, start reactivate process
        try:
            umc_page.click_details_button()
            umc_page.click_activate()
            umc_page.click_edit()
            umc_page.select_role(role="NON_HOSEL_USER")
            umc_page.click_add_role()
            return umc_page.click_save()
        except Exception as e:
            print("Exception at: " + str(e))
            return False
    else:
        return True