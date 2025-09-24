import streamlit as st
from Common.supporting import authenticate_ldap

# Pages setup
# homepage = st.Page("main_site.py", title="Home")
# umc_page = st.Page("pages/1_UMC Automation Scripts.py", title="UMC Scripts")
# # # Hide Navigation automatically if not loggedin
# st.navigation([homepage, umc_page], position="hidden")
st.set_page_config(
    page_title="Welcome to SD AutoHub",
    page_icon="👋",
    layout="wide",  # Optional: makes better use of screen space
    initial_sidebar_state="collapsed"  # This hides the sidebar by default

)
# nav = st.navigation([homepage], position="hidden")
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False


def login_page():
    st.write("# Welcome to SD Automation Hub!👋")
    # Login function
    st.title("Please login with your HCG credential")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_ldap(username, password):
            st.session_state["authenticated"] = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials.")


def main_app():
    st.sidebar.success("Select a demo above.")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()


if st.session_state["authenticated"]:
    # nav = st.navigation([homepage, umc_page], position="sidebar")
    main_app()
else:
    login_page()
