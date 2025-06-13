import time
from Sites.bsl import bsl
from Common.constant.error_message import ErrorMessage


def login_to_site(ldap_user: str, ldap_pw: str) -> bsl:
    """This is a funciton to login to Homesis with the provided username and password

    Args:
        ldap_user (str): username for LDAP
        ldap_pw (str): password for LDAP

    Returns:
        homesis: a object represent the Homesis Page in Selenium
    """
    bsl_page = bsl()
    bsl_page.get_bsl_url()
    bsl_page.login_with_data(ldap_user=ldap_user, ldap_pw=ldap_pw)
    return bsl_page


def create_bank_branch_single(bsl_page: bsl, bank_name: str, bank_branch_name: str, region: str, district: str, bank_branch_code: str) -> str:
    """This function is to create bank branch

    Args:
        bsl_page (bsl): running bsl object
        bank_name (str): string value of the bank name - used as the key value to get correct bank
        bank_branch_name (str): string value of the branch name
        region (str): string value of bank region location
        district (str): string value of bank district location
        bank_branch_code (str): string value of branch code

    Returns:
        str: error message if any
    """
    error_message = ''
    bsl_page.search_bank_name(bankname=bank_name)

    if bsl_page.click_bank_detail():
        if bsl_page.click_create_branch():
            if bsl_page.fill_branch_name(branch_name=bank_branch_name) is False:
                error_message = "Fill branch name error"
            if bsl_page.select_branch_status(value="ACTIVE") is False:
                error_message = "Select bank status error"
            if bsl_page.select_branch_region(region=region) is False:
                error_message = "Can't select bank region"
            if bsl_page.select_branch_district(district=district) is False:
                error_message = "Can't select bank district"
            if bsl_page.fill_branch_code(code=bank_branch_code) is False:
                error_message = "Fill bank branch code error"
            if bsl_page.click_OK_create_button() is False:
                error_message = "OK button error!"
            time.sleep(1.5)
        else:
            error_message = "Error when clicking create new branch!"
    else:
        error_message = "Bank not found"
    return error_message


def get_ticketing_ID() -> str:
    pass
