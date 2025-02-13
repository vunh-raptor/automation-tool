import streamlit as st
import pandas as pd
from Activity.umc_actions import (
    login_to_site,
    add_homesis_homesis_user,
    deactivate_user_with_reason,
    reactivate_user,
    remove_role,
    roles_table,
    deactivate_ra,
    check_inactive,
    add_role_umc,
    remove_role_umc,
)


def main():
    """
    This script is used for automating user account activation, deactivation, and reactivation in UMC (User Management Console).
    It utilizes the Streamlit library for creating a user interface and Selenium for interacting with the UMC web application.
    The script allows the user to input LDAP credentials, upload a CSV file containing HR codes or login names, and perform various actions on the user accounts.
    The available actions include activating accounts, deactivating accounts with a chosen reason, and reactivating accounts.
    """

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
        label="HR Code/Log In Name List",
        type=["csv", "txt"],
        accept_multiple_files=False,
    )

    # Create two columns for Active & Reactive

    active_col, _, reactive_col = st.columns(3)

    # Activate Button on the left Column
    active_account_button = active_col.button("Activate Accounts")
    # Reactivate Button on the right Column
    reactivate_account_button = reactive_col.button("Reactivate Accounts")

    # Create two columns for Deactivation Reason & Deactivate Button
    reason_col, button_col = st.columns([4, 2])

    # Reason Selection in the left column:
    deact_reason = reason_col.radio(
        label="What is the reason for Deactivation",
        options=options,
        index=0,
        captions=captions,
        key="reason_selection",
    )

    # Deactivate Button in the right column
    remove_roles_button = button_col.button(
        "Deactivate Accounts", key="deactivate_button"
    )

    # Deactivate Button in the right column
    remove_dismissal_button = button_col.button(
        "Remove Dismissal Role", key="remove_dismissal_button"
    )

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
            deactivate_user_with_reason(
                umc_page=umc_page, hr_code=hr_code, reason=reason
            )
            umc_page.get_umc_url()

    # Reactivate Account
    if reactivate_account_button:
        # Start Selenium
        umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

        # Loop through CSV & Search for HR Code
        for index, row in csv_data.iterrows():
            hr_code = row["HR Code"]
            reason = options[options.index(deact_reason)]
            reactivate_user(umc_page=umc_page, hr_code=hr_code)
            umc_page.get_umc_url()

    if remove_dismissal_button:
        # Start Selenium
        umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

        # Loop through CSV & Search for HR Code
        for index, row in csv_data.iterrows():
            hr_code = row["HR Code"]
            role = roles_table[options.index(deact_reason)]
            remove_role(umc_page=umc_page, hr_code=hr_code, role=role)
            umc_page.get_umc_url()

    st.divider()
    st.text("Deactive RA")
    deactive_ra_button = st.button("Deactive RA", type="primary")

    # deactive account
    if deactive_ra_button:
        # Start Selenium
        umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

        # Loop through CSV & Search for HR Code
        for index, row in csv_data.iterrows():
            hr_code = row["HR Code"]
            deactivate_ra(umc_page=umc_page, hr_code=hr_code)
            umc_page.get_umc_url()

    # check active account UMC
    st.divider()
    st.text("Check status account UMC")
    hr_code_input_area = st.text_area("Input Hr code here")
    hr_code_input_area_lines = hr_code_input_area.split(
        "\n"
    )  # This return a list of text area value
    check_status_btn = st.button("Check status account", type="primary")

    if check_status_btn:
        # Start Selenium
        umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
        # Initial dataframe saving user status
        data_user_status = pd.DataFrame(columns=["Hr Code", "Status"])

        # Loop through list of user input in text area
        for index in range(len(hr_code_input_area_lines)):
            hr_code = hr_code_input_area_lines[index]
            # check if user is inactive
            if check_inactive(umc_page=umc_page, hr_code=hr_code) == False:
                data_user_status = data_user_status._append(
                    {"Hr Code": hr_code, "Status": "Inactive"}, ignore_index=True
                )
            else:
                data_user_status = data_user_status._append(
                    {"Hr Code": hr_code, "Status": "Active"}, ignore_index=True
                )
            umc_page.get_umc_url()

        # display result
        left, rigth = st.columns(2, vertical_alignment="top")
        left.subheader(":red[Total result]")
        left.text("Successfully run " + str(len(hr_code_input_area_lines)) + " users")
        left.write(data_user_status)
        data_user_status_inactive = data_user_status[
            data_user_status["Status"] == "Inactive"
        ]
        rigth.subheader(":red[Inactive user]")
        rigth.write(data_user_status_inactive)

    st.divider()
    st.subheader("Add role for multiple user")
    left, rigth = st.columns(2, vertical_alignment="top")
    login_name_input_area = left.text_area("Input login name here")
    login_name_input_area_list = login_name_input_area.split("\n")  # This return a list
    role_umc_input_area = rigth.text_area("Input roles here")
    role_umc_input_area_list = role_umc_input_area.split("\n")  # This return a list
    add_role_umc_btn = st.button("Add roles UMC", type="primary")

    if add_role_umc_btn:
        # Start Selenium
        umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

        for index in range(len(login_name_input_area_list)):
            login_name = login_name_input_area_list[index]
            add_role_umc(
                umc_page=umc_page,
                login_name=login_name,
                role_list=role_umc_input_area_list,
            )
            
            umc_page.get_umc_url()
    
    st.divider()
    st.subheader("Remove role for multiple user")
    left, rigth = st.columns(2, vertical_alignment="top")
    login_name_input_area = left.text_area("Input login name to remove here")
    login_name_input_area_list = login_name_input_area.split("\n")  # This return a list
    role_umc_input_area = rigth.text_area("Input remove roles here")
    role_umc_input_area_list = role_umc_input_area.split("\n")  # This return a list
    remove_role_umc_btn = st.button("Remove roles UMC", type="primary")

    if remove_role_umc_btn:
        # Start Selenium
        umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

        for index in range(len(login_name_input_area_list)):
            login_name = login_name_input_area_list[index]
            remove_role_umc(
                umc_page=umc_page,
                login_name=login_name,
                role_list=role_umc_input_area_list,
            )
            
            umc_page.get_umc_url()


if __name__ == "__main__":
    main()
