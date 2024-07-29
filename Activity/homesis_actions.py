from Sites.homesis import homesis


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

def create_sa_account(homesis_page: homesis, hr_code: str, id_number: str, note: str, supervisor_code: str, role: str) -> bool:

    homesis_page.search_hrid(hrid=hr_code)

    if homesis_page.get_search_account_status != "Inactive":

        homesis_page.click_details_button()
        homesis_page.fill_id_number(id_number)
        homesis_page.fill_role_in_bank(role)
        homesis_page.fill_note(note)
        homesis_page.chose_supervisor(supervisor_code)
        return homesis_page.click_save_button()
    
    return False
   

