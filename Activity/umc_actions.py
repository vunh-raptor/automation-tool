from Sites.umc import umc
from Request.umc import umc_request
from Common.constant.error_message import ErrorMessage
from Common.supporting import filter_UMC_json_single_element

roles_table = [
    "NON_HOSEL_USER",
    "SALES_AGENT_MISTAKE_30DAYS",
    "SALES_AGENT_HARD_TRIGGER",
    "SALES_AGENT_TEMP_DEACTIVE",
    "SALES_AGENT_AF_DEACTIVE",
]

# Basic functions for UMC


def umc_start_session(token: str) -> umc_request:
    """This is a function to authenticate Swagger API with token from user credential

    Args:
        token (str): token of user credential

    Returns:
        umc_request: the request session
    """
    request = umc_request(token=token)
    return request


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


def add_role_umc(umc_request: umc_request, hr_codes: list, role: str) -> bool:
    """This function is used to perform add role as a datasource on UMC system

    Args:
        umc_request (umc): UMC request object
        hr_code (str): intended hr code to apply change
        role (str): the role need to add to the account

    Returns:
        bool: status of the action
    """
    return umc_request.patch_user_single_role(
        hr_codes=hr_codes, role=role.strip(), action="add")


def add_multi_role_umc(umc_request: umc_request, login_codes: list, role_list: list[str]) -> bool:
    """This function is used to perform add role by list on UMC system with fallback resolution.
    Resolves each account identifier (HR code or login name) using the check_account_status pattern.

    Args:
        umc_request (umc_request): UMC request object
        login_codes (list): list of account identifiers (HR codes or login names)
        role_list (list[str]): list of roles to add

    Returns:
        bool: status of the action
    """
    if not role_list:
        return False

    resolved_accounts = []
    for account in login_codes:
        account_id = account.strip() if isinstance(account, str) else str(account).strip()
        if account_id == "":
            continue

        username_by_hr = umc_request.get_user_info_with_hrcode(
            hr_code=account_id, element="login")
        if isinstance(username_by_hr, str) and username_by_hr.strip() != "":
            resolved_accounts.append(username_by_hr.strip())
            continue

        username_by_username = umc_request.get_user_info_with_username(
            username=account_id, element="login")
        if isinstance(username_by_username, str) and username_by_username.strip() != "":
            resolved_accounts.append(username_by_username.strip())
            continue

        resolved_accounts.append(account_id)

    if not resolved_accounts:
        return False

    success = True
    for role in role_list:
        result = umc_request.patch_user_single_role(
            login_codes=resolved_accounts, role=role.strip(), action="add")
        if not result:
            success = False

    return success


def remove_role_umc(umc_request: umc_request, login_codes: list, role: str) -> bool:
    """
    Removes a specified role from a user in the UMC page.

    This function searches for a user by their HR code, checks if the account is active,
    and if so, removes the specified role from the user. The function then saves the changes
    and verifies if the role has been successfully removed.

    Args:
        umc_request (umc): The UMC request object
        hr_code (str): The HR code of the user.
        role (str): The role to be removed from the user.

    Returns:
        bool: True if the role was successfully removed, False otherwise.
    """
    return umc_request.patch_user_single_role(hr_codes=hr_codes, role=role.strip(), action="delete")


def remove_multi_role_umc(umc_request: umc_request, login_codes: list, role_list: list[str]) -> bool:
    """This function removes all roles within a specified role list with fallback resolution.
    Resolves each account identifier (HR code or login name) using the check_account_status pattern.

    Args:
        umc_request (umc_request): The UMC request object
        login_codes (list): List of account identifiers (HR codes or login names)
        role_list (list[str]): the role list to remove

    Returns:
        bool: status of the action
    """
    if not role_list:
        return False

    resolved_accounts = []
    for account in login_codes:
        account_id = account.strip() if isinstance(account, str) else str(account).strip()
        if account_id == "":
            continue

        username_by_hr = umc_request.get_user_info_with_hrcode(
            hr_code=account_id, element="login")
        if isinstance(username_by_hr, str) and username_by_hr.strip() != "":
            resolved_accounts.append(username_by_hr.strip())
            continue

        username_by_username = umc_request.get_user_info_with_username(
            username=account_id, element="login")
        if isinstance(username_by_username, str) and username_by_username.strip() != "":
            resolved_accounts.append(username_by_username.strip())
            continue

        resolved_accounts.append(account_id)

    if not resolved_accounts:
        return False

    success = True
    for role in role_list:
        result = umc_request.patch_user_single_role(
            login_codes=resolved_accounts, role=role.strip(), action="delete")
        if not result:
            success = False

    return success


def reactivate_account(umc_request: umc_request, hr_code: str) -> bool:
    """This function reactivate the target account. Ex: Deactivated -> Activate

    Args:
        umc_request (umc_request): umc request object
        hr_code (str): the target account/hr code

    Returns:
        bool: Status of the action
    """
    return umc_request.patch_user_single_info(hr_code=hr_code, element="active", value=True)


def check_account_status(umc_request: umc_request, hr_code: str) -> str:
    """This function used to check if account is active or not

    Args:
        umc_request (umc_request): umc request object
        hr_code (str): target HR code

    Returns:
        str: Current status of the account
    """
    account_id = hr_code.strip()
    if account_id == "":
        return "NOT FOUND"

    status_by_hr_code = umc_request.get_user_info_with_hrcode(
        hr_code=account_id, element="status")
    if isinstance(status_by_hr_code, str) and status_by_hr_code.strip() != "":
        return status_by_hr_code.strip()

    status_by_username = umc_request.get_user_info_with_username(
        username=account_id, element="status")
    if isinstance(status_by_username, str) and status_by_username.strip() != "":
        return status_by_username.strip()

    return "NOT FOUND"

def get_account_username(umc_request: umc_request, hr_code: str) -> str:
    """This function used to get account username

    Args:
        umc_request (umc_request): umc request object
        hr_code (str): hr code of the intended account

    Returns:
        str: account username of the hrcode
    """
    return umc_request.get_user_info_with_hrcode(hr_code=hr_code, element="login")

# --------------------------------------------------------------------------------------------------------------
# Specific-case function


def add_homesis_homesis_user(umc_request: umc_request, hr_codes: list) -> bool:
    """This is a function to active a user and adding HOMESIS and HOMESIS_USER as his owned roles

    Args:
        umc_page (umc): current active umc session
        hr_code (str): the target HR Code

    Returns:
        bool: status of the role adding action
    """
    return add_multi_role_umc(umc_request=umc_request, login_codes=hr_codes, role_list=["HOMESIS", "HOMESIS_USER"])


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
        return umc_page.verify_updated_info()
    return False


def deactivate_ra(umc_request: umc_request, hr_code: str) -> bool:
    """_Deactive a specific RA account in UMC page

    Args:
        umc_request (umc_request): The UMC request object
        hr_code (str): The HR code of the user.

    Returns:
        bool: True if successfully click the deactive button
    """
    return umc_request.patch_user_single_info(hr_code=hr_code, element="active", value=False)


def update_phone_number(umc_page: umc, hr_code: str, phone_number: str) -> list:
    """This function used to update phone number for target account

    Args:
        umc_page (umc): The UMC selenium object
        hr_code (str): target HR code
        phone_number (str): new phone number

    Returns:
        list: list of error
    """
    list_of_error = []
    umc_page.search_hrid(hrid=hr_code)
    # Get account Status before running
    account_status = umc_page.get_search_account_status()
    # Check if account is Inactive
    if account_status == "Inactive":
        list_of_error.append(
            hr_code + " - " + ErrorMessage.umc_message.USER_INACTIVE)
    if account_status == "Account not found":
        list_of_error.append(
            hr_code + " - " + ErrorMessage.umc_message.USER_NOT_FOUND)
    if account_status == "Active":
        # Account found, start update date of birth actions
        umc_page.click_details_button()
        umc_page.click_edit()
        umc_page.update_info(data=phone_number, field=umc_page.detail_mobile)
        umc_page.update_info(data=phone_number, field=umc_page.detail_phone)
        umc_page.click_save()
        # Check if Update successfully
        list_of_error.append(
            hr_code + " - " + ErrorMessage.umc_message.USER_UPDATED)
    return list_of_error

def update_name(umc_request: umc_request, hr_code: str, first_name: str, last_name: str) -> bool:
    """This function is to update first name and last name of the user

    Args:
        umc_request (umc_request): The UMC request object
        hr_code (str): hr code of the user
        first_name (str): value to change - First Name
        last_name (str): value to change - Last Name

    Retry Mechanism:
    If the update using the HRcode is failed by not found (response 404), then the code will try to use username to do the update

    Returns:
        bool: status of the action
    """
    retry = False
    result = umc_request.patch_user_firstname_lastname(hr_code=hr_code, first_name=first_name, last_name=last_name)
    if result is False:
        username = get_account_username(umc_request=umc_request, hr_code=hr_code)
        retry = True
        result = umc_request.patch_user_firstname_lastname(hr_code=username, first_name=first_name, last_name=last_name)
    if result is False and retry is True:
        return False
    return True

def update_dob(umc_page: umc, hr_code: str, date_of_birth: str) -> list:
    """ Update date of birth for account LDAP

    Args:
        umc_page (umc): login to UMC pasge
        hr_code (str): HR code format 000xxxx or HCG account A.NguyenV
        date_of_birth (str): date of birth format: yyyy-mm-dd

    Returns:
        list: replace and update new DOB
    """
    list_of_error = []
    umc_page.search_hrid(hrid=hr_code)
    # Get account Status before running
    account_status = umc_page.get_search_account_status()
    # Check if account is Inactive
    if account_status == "Inactive":
        list_of_error.append(
            hr_code + " - " + ErrorMessage.umc_message.USER_INACTIVE)
    if account_status == "Account not found":
        list_of_error.append(
            hr_code + " - " + ErrorMessage.umc_message.USER_NOT_FOUND)
    if account_status == "Active":
        # Account found, start update date of birth actions
        umc_page.click_details_button()
        umc_page.click_edit()
        umc_page.update_info(data=date_of_birth, field=umc_page.date_of_birth)
        umc_page.click_save()
        # Check if Update successfully
        list_of_error.append(
            hr_code + " - " + ErrorMessage.umc_message.USER_UPDATED)
    return list_of_error


def update_gender(umc_page: umc, hr_code: str, detail_gender: str) -> list:
    """ Update gender for account LDAP

    Args:
        umc_page (umc): login to UMC page
        hr_code (str): HR code format 000xxxx or HCG account A.NguyenV
        detail_gender (str): detail gender format male or female

    Returns:
        list: replace and update gender for account LDAP
    """
    list_of_error = []
    umc_page.search_hrid(hrid=hr_code)
    # Get account Status before running
    account_status = umc_page.get_search_account_status()
    # Check if account is Inactive
    if account_status == "Inactive":
        list_of_error.append(
            hr_code + " - " + ErrorMessage.umc_message.USER_INACTIVE)
    if account_status == "Account not found":
        list_of_error.append(
            hr_code + " - " + ErrorMessage.umc_message.USER_NOT_FOUND)
    if account_status == "Active":
        # Account found, start update gender actions
        umc_page.click_details_button()
        umc_page.click_edit()
        umc_page.update_info(data=detail_gender, field=umc_page.detail_gender)
        umc_page.click_save()
        # Check if Update successfully
        list_of_error.append(
            hr_code + " - " + ErrorMessage.umc_message.USER_UPDATED)
    return list_of_error


def update_employed_since(umc_request: umc_request, hr_code: str, employedSince: str) -> bool:
    """Update employed since for account LDAP

    Args:
        umc_request (umc_request): The UMC request object
        hr_code (str): hr code of the target account
        employedSince (str): the contract signed date that we need to change

    Returns:
        bool: status of the action
    """
    return umc_request.patch_user_single_info(hr_code=hr_code, element="startDate", value=employedSince)


def update_mail(umc_page: umc, hr_code: str, mail: str) -> list:
    """ Update mail for account LDAP

    Args:
        umc_request (umc_request): UMC request object
        hr_code (str): HR code format 000xxxx, RAxxxx, FPTxxx or HCG account ex: A.NguyenV
        mail (str): input mail to account UMC ex: abc@doamin.com

    Returns:
        list: replace and update mail for account LDAP
    """
    list_of_error = []
    umc_page.search_hrid(hrid=hr_code)
    # Get account Status before running
    account_status = umc_page.get_search_account_status()
    # Check if account is Inactive
    if account_status == "Inactive":
        list_of_error.append(
            hr_code + " - " + ErrorMessage.umc_message.USER_INACTIVE)
    if account_status == "Account not found":
        list_of_error.append(
            hr_code + " - " + ErrorMessage.umc_message.USER_NOT_FOUND)
    if account_status == "Active":
        # Account found, start update gender actions
        umc_page.click_details_button()
        umc_page.click_edit()
        umc_page.update_info(data=mail, field=umc_page.mail)
        umc_page.click_save()
        # Check if Update successfully
        list_of_error.append(
            hr_code + " - " + ErrorMessage.umc_message.USER_UPDATED)
    return list_of_error


def create_RA_account(umc_request: umc_request):
    pass


def get_deactivation_date(umc_request: umc_request, hr_code: str) -> str:
    """This fuction is used to get deactivation date

    Args:
        umc_request (umc_request): request session of the UMC
        hr_code (str): hr_code of the user

    Returns:
        str: status
    """

    return f"Deactivation Time: {filter_UMC_json_single_element(response=umc_request.get_account_raw_data(hr_code=hr_code), element='lastDeactivationTime').split('T')[0]}"

def get_employedsince_date(umc_request: umc_request, hr_code: str) -> str:
    """This function is used to get employed since date

    Args:
        umc_request (umc_request): request session of the UMC
        hr_code (str): hr_code of the user

    Returns:
        str: status
    """

    return f"Employed Since: {filter_UMC_json_single_element(response=umc_request.get_account_raw_data(hr_code=hr_code), element='employedSince').split('T')[0]}"