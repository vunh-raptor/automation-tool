import time
from Sites.idm import idm


def login_to_site() -> idm:
    idm_page = idm()
    idm_page.get_idm_url()
    idm_page.click_login_button()
    return idm_page


def search_user_by_login_name(idm_page: idm, user_login_name: str) -> bool:
    time.sleep(1)
    idm_page.click_view_user_extended()
    time.sleep(1)
    idm_page.click_choose_search_user_type_of_info()
    idm_page.choose_search_user_by_login_name_option()
    time.sleep(1)
    idm_page.input_search_value_field(user_login_name)
    time.sleep(1)
    return idm_page.click_idm_search_button()


def search_user_by_hr_code(idm_page: idm, user_login_name: str) -> bool:
    time.sleep(1)
    idm_page.click_view_user_extended()
    time.sleep(1)
    idm_page.click_choose_search_user_type_of_info()
    idm_page.choose_search_user_by_hr_code_option()
    time.sleep(1)
    idm_page.input_search_value_field(user_login_name)
    time.sleep(1)
    return idm_page.click_idm_search_button()


def search_user_in_modify(idm_page: idm, user_login_name: str) -> bool:
    time.sleep(1)
    idm_page.click_view_user_modify()
    time.sleep(1)
    idm_page.input_search_value_field(user_login_name)
    time.sleep(1)
    return idm_page.click_idm_search_button_in_modify_page()


def access_user_profile(idm_page: idm) -> bool:
    time.sleep(1)
    return idm_page.click_user_select_button()


def get_user_info(idm_page: idm, element_id: str) -> str:
    time.sleep(2)
    return idm_page.get_element_value_by_id(element_id)
