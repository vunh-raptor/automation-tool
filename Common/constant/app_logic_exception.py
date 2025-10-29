import streamlit as st
from enum import Enum


class AppLogicExceptionHandler(Enum):
    LOGIN_ERROR = "Invalid username and password. Please try again."
    CSV_ERROR = "Invalid CSV. Check your CSV file again."
    GENERIC_ERROR = "Something went wrong. Please try again."


class LoginError(Exception):
    pass


def app_logic_exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LoginError as le:
            st.error(AppLogicExceptionHandler.LOGIN_ERROR.value)
            st.exception(le)
        except UnboundLocalError as ule:
            st.error(AppLogicExceptionHandler.CSV_ERROR.value)
            st.exception(ule)
        except Exception as e:
            st.error(AppLogicExceptionHandler.GENERIC_ERROR.value)
            st.exception(e)
    return wrapper
