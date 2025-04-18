import pytest
import unittest
from Common.supporting import (
    generate_OTP,
    cyberark_get_credential_password,
    bsl_bank_name_crosscheck,
)


class TestGeneralFunctions(unittest.TestCase):
    def setUp(self):
        """
        This function is to declare initialize variables for test function will use, or even the initialized variables can be used to compare status
        """
        self.OTP_len = 6
        self.sample_bank_name = "VPBANK - Ngân hàng TMCP Việt Nam Thịnh Vượng"

    def test_get_generate_OTP(self):
        """
        Test if generate OTP function is working correctly
        Test Success: length of the result equals length of a normal 6 digits OTP
        """
        test_OTP = generate_OTP()
        result = test_OTP.now()
        assert len(result) == self.OTP_len

    def test_get_credential_CBA(self):
        """
        Test if function query CBA credential in password vault is working correctly
        Test Success: length of the result more than 10, indicate password has been queried and not return any empty response. Also one more condition is no Powershell error response like Invoke
        """
        result = cyberark_get_credential_password()
        assert len(result) > 10 or "Invoke" not in result

    def test_crosscheck_bank_name(self):
        """
        Test if function cross check bank name is working properly
        Test Success: return True when the bank name is found on list
        """
        preload_path = r"Common\data\bank_list.txt"
        f = open(preload_path, "r", encoding="utf8")
        bank_name_list = f.readlines()
        result = bsl_bank_name_crosscheck(
            bank_name_list=bank_name_list, bank_name=self.sample_bank_name)
        assert result is True
