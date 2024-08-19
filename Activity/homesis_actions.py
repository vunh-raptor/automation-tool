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


#This funtion is to add role in bank for RA
def add_role_in_bank_RA(homesis_page: homesis, hr_code: str, id_number: str, note: str, supervisor_code: str, role: str) -> list:
    list_of_error = []
    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():
        if homesis_page.fill_id_number(id_number) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ID_NUMBER)
        if homesis_page.fill_role_in_bank(role) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ROLE)
        if homesis_page.fill_note(note) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_NOTE)
        if homesis_page.chose_supervisor(supervisor_code) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FIND_SUP_CODE)
        if homesis_page.click_save_button():
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CLICK_SAVE_BUTTON)
    else:
        list_of_error.append(hr_code + "-" + ErrorMessage.homesis_message.CAN_NOT_FIND_USER)
    return list_of_error

#This funtion is to add role in bank for SA 
def add_role_in_bank_SA(homesis_page: homesis, hr_code: str, id_number: str, note: str, supervisor_code: str, role: str, location : str) -> list:
    list_of_error = []
    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():                 
        if homesis_page.fill_id_number(id_number) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ID_NUMBER)
        if homesis_page.fill_role_in_bank(role) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ROLE)
        if homesis_page.fill_note(note) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_NOTE)
        if homesis_page.select_location(location):
            homesis_page.click_add_location()
            time.sleep(1)
            homesis_page.click_add_assign_district()
            time.sleep(1)
        else:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FIND_LOCATION)
        if homesis_page.chose_supervisor(supervisor_code) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FIND_SUP_CODE)
        if homesis_page.click_save_button():
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CLICK_SAVE_BUTTON)
    else:
        list_of_error.append(hr_code + "-" + ErrorMessage.homesis_message.CAN_NOT_FIND_USER)
    return list_of_error

#This funtion is to add role in bank for RA MW
def add_role_in_bank_RA_MW(homesis_page: homesis, hr_code: str, note: str, role: str) -> list:
    list_of_error = []
    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():
        if homesis_page.fill_role_in_bank(role) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ROLE)
        if homesis_page.fill_note(note) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_NOTE)
        if homesis_page.click_save_button():
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CLICK_SAVE_BUTTON)  
    else:
        list_of_error.append(hr_code + "-" + ErrorMessage.homesis_message.CAN_NOT_FIND_USER)    
    return list_of_error

#This funtion is to add role in bank for RA FPT
def add_role_in_bank_RA_FPT(homesis_page: homesis, hr_code: str, note: str, id_number: str, role: str) -> list:
    list_of_error = []
    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():
        if homesis_page.fill_role_in_bank(role) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ROLE)
        if homesis_page.fill_id_number(id_number) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ID_NUMBER)
        if homesis_page.fill_note(note) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_NOTE)
        if homesis_page.click_save_button():
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CLICK_SAVE_BUTTON)
    else:
        list_of_error.append(hr_code + "-" + ErrorMessage.homesis_message.CAN_NOT_FIND_USER)    
    return list_of_error

#This funtion is to add role in bank for RA New Segment
def add_role_in_bank_RA_New_Segment(homesis_page: homesis, hr_code: str, note: str, id_number: str, role: str, supervisor_code: str) -> list:
    list_of_error = []
    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.click_details_button():
        if homesis_page.fill_id_number(id_number) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ID_NUMBER)
        if homesis_page.fill_role_in_bank(role) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_ROLE)
        if homesis_page.fill_note(note) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FILL_NOTE)
        if homesis_page.chose_supervisor(supervisor_code) == False:
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CAN_NOT_FIND_SUP_CODE)
        if homesis_page.click_save_button():
            list_of_error.append(hr_code + " - " + ErrorMessage.homesis_message.CLICK_SAVE_BUTTON)    
    return list_of_error
