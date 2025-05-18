import pytest
from Common.supporting import (
    cyberark_get_credential_password,
    generate_OTP
)
from Activity.umc_actions import (
    add_role_umc,
    remove_single_role,
    remove_multi_roles_umc,
    check_account_status,
    login_to_site,
)

# Initialize Global Object to start test

# def capture_test_status(func):
#     def wrapper(*args, **kwargs):
#         try:
#             func(*args, **kwargs)
#             return f"{func.__name__} - Test Success"
#         except AssertionError as e:
#             return f"{func.__name__} - Test Failed: {str(e)}"
#         return wrapper


# def test_login_umc():
#     try:
#         assert test_get_credential_CBA is not AssertionError
#         assert login_to_site(
#             ldap_user="umc_admin1", ldap_pw=cyberark_get_credential_password()) is not None
#         return "Initialize UMC Login - Test Success"
#     except AssertionError:
#         return "Initialize UMC Login - Test Failed"


# def test_check_account_status():
#     try:
#         result = check_account_status(
#             active_umc_session, "00051359")
#         assert result in ["Active", "Inactive",
#                           "Not found"], f"Unexpected account status: {result}"
#     except Exception as e:
#         raise AssertionError("UMC Check Account Status - Test Failed")
