from pandas import DataFrame, read_excel
import json
from requests import Response
import logging
from pyotp import TOTP
from msteamsapi import AdaptiveCard, Container, TeamsWebhook, ContainerStyle


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


def push_error_to_MSTeams(webhook: str) -> None:
    pass

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


def generate_OTP():
    """This function used to generate OTP and send to MSteams

    Returns:
        str: the generated OTP
    """
    try:
        timeOTP = TOTP('base32secret3232', interval=600)

        # Assign the Power Automate Webhook
        webhook = TeamsWebhook(
            "https://prod-102.westeurope.logic.azure.com:443/workflows/622b616dc2a9428e9dfa90b97df7a5c2/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=7J64W7hby4vALfHoRosepx0voq-jJd-KB0Nzepfgu0Y")

        # Build & send the message card
        card = AdaptiveCard(title="Reactivate OTP",
                            title_style=ContainerStyle.DEFAULT)
        container = Container(style=ContainerStyle.DEFAULT)
        container.add_text_block(text="Generated OTP: " + timeOTP.now())
        card.add_container(container=container)
        webhook.add_cards(card)
        webhook.send()

        # return the OTP value to compare in the verify_OTP function
        return timeOTP
    except Exception as e:
        print(e)


def verify_OTP(sourceOTP: TOTP, OTP: str) -> bool:
    """This function used to verify OTP when input

    Args:
        OTP (str): the OTP that SD input to verify

    Returns:
        bool: the status of the verification
    """
    try:
        return sourceOTP.verify(OTP)
    except Exception as e:
        print(e)
        return False
