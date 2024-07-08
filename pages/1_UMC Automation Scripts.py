import streamlit as st
import pandas as pd
from Activity.umc_actions import *


# Radio button options
options = [
    "Resignation",
    "Mistake 30 Days",
    "Hard trigger",
    "Deactivation Temporarily",
    "Antifraud Decision",
]

captions = [
    "Remove all roles + Add NON_HOSEL_USER",
    "Remove all roles + Add SALES_AGENT_MISTAKE_30DAYS",
    "Remove all roles + Add SALES_AGENT_HARD_TRIGGER",
    "Remove all roles + Add SALES_AGENT_TEMP_DEACTIVE",
    "Remove all roles + Add SALES_AGENT_AF_DEACTIVE",
]

# Username & Password Input
ldap_user = st.text_input("LDAP USERNAME")
ldap_pw = st.text_input("LDAP PASSWORD", type="password")

# List HR Code/Login Name Input
csv_upload = st.file_uploader(
    label="HR Code/Log In Name List", type=["csv", "txt"], accept_multiple_files=False
)

# Activate Button
active_account_button = st.button("Activate Accounts - Adding HOMESIS & HOMESIS_USER")

# Reason Selection:
deact_reason = st.radio(
    label="What is the reason for Deactivation",
    options=options,
    index=0,
    captions=captions,
)

# Deactivate Button
remove_roles_button = st.button("Deactivate Accounts with The Chosen Reason")

# Reactivate Button
reactivate_account_button = st.button("Reactivate Accounts")


# Read CSV Data
if csv_upload is not None:
    csv_data = pd.read_csv(csv_upload, converters={"HR Code": str})
    result_table = st.write(csv_data)

# Activate Account
if active_account_button:
    # Start Selenium
    umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

    # Loop through CSV & Search for HR Code
    for index, row in csv_data.iterrows():
        hr_code = row["HR Code"]
        add_homesis_homesis_user(umc_page=umc_page, hr_code=hr_code)
        umc_page.get_umc_url()


# Deactivate Account
if remove_roles_button:
    # Start Selenium
    umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

    # Loop through CSV & Search for HR Code
    for index, row in csv_data.iterrows():
        hr_code = row["HR Code"]
        reason = roles_table[options.index(deact_reason)]
        deactivate_user_with_reason(umc_page=umc_page, hr_code=hr_code, reason=reason)
        umc_page.get_umc_url()

# Reactivate Account
if reactivate_account_button:
     # Start Selenium
    umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

    # Loop through CSV & Search for HR Code
    for index, row in csv_data.iterrows():
        hr_code = row["HR Code"]
        reason = roles_table[options.index(deact_reason)]
        reactivate_user(umc_page=umc_page, hr_code=hr_code)
        umc_page.get_umc_url()
