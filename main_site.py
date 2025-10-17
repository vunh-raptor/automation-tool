import streamlit as st
from Common.supporting import authenticate_ldap, logout_render, request_to_automate_button

# Pages setup
# homepage = st.Page("main_site.py", title="Home")
# umc_page = st.Page("pages/1_UMC Automation Scripts.py", title="UMC Scripts")
# # # Hide Navigation automatically if not loggedin
# st.navigation([homepage, umc_page], position="hidden")
st.set_page_config(
    page_title="Welcome to SD AutoHub",
    page_icon="👋",
    layout="wide",  # Optional: makes better use of screen space
    initial_sidebar_state="collapsed",  # This hides the sidebar by default
    menu_items={"Get help": None,
                "About": "Developed and maintained by: **Service Desk Team** with Tech Leader: **Nhu.HuynhNY**"}
)
# nav = st.navigation([homepage], position="hidden")
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["userDisplayName"] = ""
    st.session_state["autoreq"] = False


def login_page():
    st.write("# Welcome to SD Automation Hub!👋")
    # Login function
    st.title("Please login with your HCG credential")
    with st.form("loginForm"):
        st.warning(
            "Please request role VN.SD.SD_AUTOMATION_HUB.USER on IDM if you need access")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            displayName = authenticate_ldap(username, password)
            if len(displayName) > 0:
                st.session_state["authenticated"] = True
                st.session_state["userDisplayName"] = displayName
                st.rerun()
            else:
                st.error("Invalid credentials or lack of permission")


if st.session_state["authenticated"]:
    # nav = st.navigation([homepage, umc_page], position="sidebar")
    st.success("Login success! Welcome " +
               str(st.session_state["userDisplayName"]))
    request_to_automate_button()
    logout_render()
else:
    login_page()
