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


def filter_UMC_json_single_element(response: Response, element: str) -> str:
    """This function is to support getting the intended element from the response of the API

    Args:
        response (Response): Response from the API

    Returns:
        dict: ID from the response
    """

    try:
        json_obj = json.loads(response.text)
        for fields in json_obj["data"]:
            return fields[f'{element}']
    except Exception as e:  # noqa: E722
        print("File Error, file not found!\n")
        return ""  # Return an empty dictionary if an exception occurs
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
    """This function is used to authenticate with Home Credit Credential with AD LDAP

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


def authenticate_swagger(username: str, password: str) -> str:
    """This function is to used to authenticate to HOSEL Swagger APIs

    Args:
        username (str): username of the user
        password (str): password of the user

    Returns:
        str: Base64 encoded token to use in Swagger
    """
    from base64 import b64encode
    credentials = f"{username}:{password}"
    credentials_encode = f"Basic {b64encode(credentials.encode()).decode()}"
    print(credentials_encode)
    return credentials_encode

# Front End Generations


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


def request_to_automate_button():
    """This is function to submit Request to automate your work
    """
    if "autoreq" not in st.session_state:
        st.session_state["autoreq"] = False
    if st.sidebar.button("Request to automate"):
        st.session_state["autoreq"] = True

    if st.session_state["autoreq"] is True:
        request_to_automate()


@st.dialog("Request to automate", width="large")
def request_to_automate():
    """Display the contribution form dialog"""
    st.markdown("Fill in the details below to create a JIRA Request.")

    with st.form("contribution_form", clear_on_submit=True):
        # Summary field
        summary = st.text_input(
            "Summary *",
            placeholder="Enter a brief summary",
            help="Brief summary of the request to automate"
        )

        # Description field
        description = st.text_area(
            "Description *",
            placeholder="Enter detailed description",
            height=120,
            help="Detailed description of the request to automate"
        )

        # File uploader for attachments
        attachments = st.file_uploader(
            "Picture Attachments",
            type=["png", "jpg", "jpeg", "gif"],
            accept_multiple_files=True,
            help="Upload files (optional)"
        )

        # Display uploaded files
        if attachments:
            st.markdown("**Uploaded files:**")
            for file in attachments:
                st.markdown(f"- {file.name} ({file.size / 1024:.1f} KB)")

        # Form buttons
        col1, col2 = st.columns([1, 5])

        with col1:
            cancel_button = st.form_submit_button(
                "Cancel", use_container_width=True)

        with col2:
            submit_button = st.form_submit_button(
                "Submit",
                type="primary",
                use_container_width=True
            )

        # Handle form submission
        if submit_button:
            if not summary or not description:
                st.error(
                    "Please fill in all required fields (Summary and Description)")
                st.session_state["autoreq"] = False
            else:
                st.session_state["autoreq"] = False
            st.session_state["autoreq"] = False
        if cancel_button:
            st.session_state["autoreq"] = False
