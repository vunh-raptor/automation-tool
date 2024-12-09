from jira import JIRA
from jira_insight import Insight
from pandas import DataFrame, read_excel
from streamlit.runtime.uploaded_file_manager import UploadedFile
import logging



def __auth_gen(file: UploadedFile = None, path: str = None) -> tuple:
    """The basic account/password reader from file. The UploadedFile from Streamlit will be prioritized.

    Args:
        file (UploadedFile, optional): The UploadedFile, read from streamlit.file_uploader. Defaults to None.
        path (str, optional): The Path to the account file. Defaults to None.

    Returns:
        tuple: a pair of username and password.
    """
    try:
        if UploadedFile != None:
            account_data = UploadedFile.readlines()
        else:
            file = open(path, "r")
            account_data = file.readlines()

        if len(account_data) < 2:
            logging.critical("Cannot find the account information at " + path)
            return None

        username = account_data[0].replace("\n", "").replace("\r", "")
        password = account_data[1].replace("\n", "").replace("\r", "")
        basic_auth = (username, password)

        return basic_auth

    except Exception as e:
        logging.critical(e)
        return None


def jira_Auth(
    file: UploadedFile = None,
    path: str = "jira_account.txt",
    jira_server: str = "https://servicedesk.homecredit.net",
) -> JIRA:
    """JiraSD authentication which returns JIRA element

    Args:
        path (str, optional): path to text file. Defaults to "jira_account.txt".
        jira_server (_type_, optional): hostname of JiraSD page. Defaults to "https://servicedesk.homecredit.net".

    Returns:
        JIRA: Jira element which authenticated and can be function on Home Credit JiraSD
    """
    try:
        basic_auth = __auth_gen(file=file, path=path)
        options = {"server": jira_server}
        jira = JIRA(options=options, basic_auth=basic_auth)
        return jira
    except Exception as e:
        logging.critical(e)  # noqa: E722
        logging.critical("Login failed! Check Jira SVC Bot username and account")


def jira_insight_Auth(
    file: UploadedFile = None,
    path: str = "jira_account.txt",
    jira_server: str = "https://servicedesk.homecredit.net",
) -> Insight:
    """JiraSD authentication which returns JIRA Insight element

    Args:
        path (str, optional): path to text file. Defaults to "jira_account.txt".
        jira_server (_type_, optional): hostname of JiraSD page. Defaults to "https://servicedesk.homecredit.net".

    Returns:
        Insight: Jira Insight element which authenticated and can be function on Home Credit JiraSD
    """
    try:
        basic_auth = __auth_gen(file=file, path=path)
        insight = Insight(jira_server, basic_auth=basic_auth)
        return insight
    except Exception as e:
        logging.critical(e)  # noqa: E722
        logging.critical("Login failed! Check Jira SVC Bot username and account")


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

def bsl_bank_name_crosscheck(bank_name_list: list, bank_name:str) -> bool:
    """This function to support Bank name crosschecking to verify if the data is valid, if not then it will return False to BSL_Automation Scripts take action

    Args:
        read_path (str): text file of bank data
        bank_name (str): string value of bank name to compare

    Returns:
        bool: result of the bank name lookup - If true is found, if False is not found
    """
    try:
        for name in bank_name_list:
            print(name.strip())
            print(bank_name.strip())
            if bank_name.strip() == name.strip():
                return True
            continue
        return False
    except ValueError:
        logging.critical("Cannot write or read file")
    except:  # noqa: E722
        logging.critical("File Error, file not found!")
        return False