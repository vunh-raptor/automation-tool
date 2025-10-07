from pandas import DataFrame, read_excel
import streamlit as st
import json
from requests import Response
import logging
from pyotp import TOTP
from msteamsapi import AdaptiveCard, Container, TeamsWebhook, ContainerStyle
from ldap3 import Server, Connection, ALL, SUBTREE

REACTIVATE_WEBHOOK_URL = "https://prod-102.westeurope.logic.azure.com:443/workflows/622b616dc2a9428e9dfa90b97df7a5c2/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=7J64W7hby4vALfHoRosepx0voq-jJd-KB0Nzepfgu0Y"
ERROR_WEBHOOK_URL = "https://default5675d32119d14c9596842c28ac8f80.a4.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/2441849b00aa40dfbfd4badcc9f748d3/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ypI1uwC9FCskpObxzJxKqzZD85tSs2lTYV5QfrDcdWs"


def support_Excel_read(read_path: str, sheet_name: str = "Sheet1") -> DataFrame:
    """This function is to support reading Excel file on xlsx attachment

    Args:
        read_path (str): File to read location
        sheet_name (str, optional): Sheet name for pandas to perform read. Defaults to "Sheet1".

    Returns:
        DataFrame: Data for script to function
    """
    try:
        df = read_excel(read_path, sheet_name)
        return df
    except ValueError:
        logging.critical("Cannot write or read file")
    except:  # noqa: E722
        logging.critical("File Error, file not found!")
        return df[:0]


def push_msg_to_MSTeams(adaptiveCard: AdaptiveCard, webhook_url: str = ERROR_WEBHOOK_URL) -> bool:
    try:
        webhook = TeamsWebhook(webhook_url=webhook_url)
        webhook.add_cards(adaptiveCard)
        webhook.send()
        return True
    except Exception as e:
        print(e)
        return False


def adaptive_card_build_MSteams(msg_title: str, **kwargs) -> AdaptiveCard:
    try:
        card = AdaptiveCard(
            title=msg_title, title_style=ContainerStyle.DEFAULT)
        container = Container(style=ContainerStyle.DEFAULT)
        if kwargs:
            for value in kwargs.values():
                container.add_text_block(value)
        card.add_container(container=container)
        return card
    except Exception as e:
        print(e)
    return None  # type: ignore

# BSL Section


def bsl_bank_name_crosscheck(bank_name_list: list, bank_name: str) -> bool:
    """This function to support Bank name crosschecking to verify if the data is valid, if not then it will return False to BSL_Automation Scripts take action

    Args:
        read_path (str): text file of bank data
        bank_name (str): string value of bank name to compare

    Returns:
        bool: result of the bank name lookup - If true is found, if False is not found
    """
    try:
        for name in bank_name_list:
            if bank_name.strip().lower() == name.strip().lower():
                return True
            continue
        return False
    except ValueError:
        logging.critical("Cannot write or read file")
    except:  # noqa: E722
        logging.critical("File Error, file not found!")
        return False

# JIRA Response Section


def filter_id_from_response(response: Response) -> dict:
    """This function is to support getting the ID from the response of the API

    Args:
        response (Response): Response from the API

    Returns:
        dict: ID from the response
    """
    return_dict = {}

    try:
        json_obj = json.loads(response.text)
        for fields in json_obj['transitions']:
            return_dict[fields['name']] = fields['id']
        return return_dict
    except Exception as e:  # noqa: E722
        print("File Error, file not found!\n")
        print(e)
        return {}  # Return an empty dictionary if an exception occurs

# def filter_linked_tickets_from_response(response: Response) -> dict:
#     """This function is to support getting the linked ticket ID & it's summary from the response of the API

#     Args:
#         response (Response): Response from the API

#     Returns:
#         dict: {ID - Summary} - Example: {APPROVALVN-12313 - Approval for SRVN}
#     """
#     return_dict = {}
#     try:
#         json_obj = json.loads(response.text)
#         for fields in json_obj['fields']['issuelinks']:
#             return_dict[fields['outwardIssue']['key']] = fields['outwardIssue']['fields']['summary']
#         return return_dict
#     except Exception as e:  # noqa: E722
#         print(e)
#         return {}


def cyberark_get_credential_password() -> str:
    """This function is to get credential password stored on CyberArk Password Vault

    Args:
        requestCredential (str): the credential that the script needs to get on CyberArk Vault
        certThumbprint (str): Network certificate thumbprint of current users

    Returns:
        str: the password value of the credential
    """
    result = ""
    powershell_script = "Common\\data\\CBAAccess.ps1"
    try:
        result = powershell_run_output(script_path=powershell_script)
        return result.replace("\n", "")
    except Exception as e:
        print(e)
        return ""


def system_env_get_cred() -> str:
    """This function is to get credential password stored on System Variables

    Returns:
        str: password value of the credential
    """
    from os import environ
    result = ""
    try:
        result = environ['UMCAdminCred']
        return result
    except Exception as e:
        print(e)
        return ""


def powershell_run_output(script_path: str) -> str:
    """This function to run Powershell cmd - return output

    Args:
        cmd (str): powershell command

    Returns:
        str: output of the powershell command
    """
    from subprocess import run
    try:
        completed = run(["powershell", "-File", script_path],
                        capture_output=True, encoding="utf-8")
        return str(completed.stdout)
    except Exception as e:
        print(e)
        return ""

# OTP Generating and verifying functions


def generate_OTP():
    """This function to generate OTP

    Returns:
        TOTP: the variable of time OTP that can be pass down to used for verification
    """
    try:
        # Generate OTP fucntion
        timeOTP = TOTP('base32secret3232', interval=600)
        # Build & send the message card
        card = adaptive_card_build_MSteams(msg_title="Reactivate OTP", param1="Generated OTP: " +
                                           timeOTP.now(), param2="Requestor: " + str(st.session_state["userDisplayName"]))
        push_msg_to_MSTeams(
            webhook_url=REACTIVATE_WEBHOOK_URL, adaptiveCard=card)

        # return the OTP value to compare in the verify_OTP function
        return timeOTP
    except Exception as e:
        print(e)


def verify_OTP(sourceOTP: TOTP, OTP: str) -> bool:
    """This function used to verify OTP when input

    Args:
        sourceOTP (TOTP): the source OTP that were passdown in the previous generate_OTP function
        OTP (str): the OTP that SD input to verify

    Returns:
        bool: the status of the verification
    """
    try:
        return sourceOTP.verify(OTP)
    except Exception as e:
        print(f"Error when calling to OTP fucntions: {e}")
        return False

# Authentication functions


def authenticate_ldap(username: str, password: str) -> str:
    """This function is used to authenticate with Home Credit Credential with LDAP

    Args:
        username (str): username of the user
        password (str): password of the user

    Returns:
        bool: the status of the login request, True if success login and False if failed login
    """
    try:
        userDN = ""
        server = Server("ldap://vn-ldaps.hcg.homecredit.net", get_info=ALL)
        conn = Connection(
            server, f"CN={username},OU=Users,OU=VN,DC=hcg,DC=homecredit,DC=net", f"{password}", auto_bind=True)
        if conn.bound:
            conn.search(search_base="OU=Users,OU=VN,DC=hcg,DC=homecredit,DC=net",
                        search_filter=f"(&(samAccountName={username})(memberOf=CN=VN.SD.SD_AUTOMATION_HUB.USER,OU=Groups,OU=VN,DC=hcg,DC=homecredit,DC=net))", search_scope=SUBTREE, attributes="displayName")
            userDN = conn.entries[0].displayName
            conn.unbind()
            return userDN
        else:
            conn.unbind()
            return ""
    except Exception as e:
        print(f"Error when calling to LDAP server: {e}")
        return ""


def login_status_check():
    """This is a quick function to constantly check if user is authenticated
    """
    if st.session_state["authenticated"] is not True:
        st.switch_page("main_site.py")


def logout_render():
    """This is function to render logout button
    """
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()
