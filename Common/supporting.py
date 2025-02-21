from pandas import DataFrame, read_excel
import json
from streamlit.runtime.uploaded_file_manager import UploadedFile
from requests import Response
import logging


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