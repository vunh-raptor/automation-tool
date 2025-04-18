import streamlit as st
import pytest


def main():
    st.write("This page is used to performed automation tests")
    test_UMC_button = st.button("Test UMC function")

    if test_UMC_button:
        test_file_path = "Tests/General_Automation_unit_test.py"
        result = pytest.main([test_file_path, "-rA"])
        if result == 0:
            st.write("General functions - All Tests successful!")
        elif result == 1:
            st.write("General functions - Some Tests failed!")
        elif result == 3:
            st.write("General functions - Test failed - Internal error detected!")


if __name__ == "__main__":
    main()
