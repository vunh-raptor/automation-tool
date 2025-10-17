from Common.supporting import (
    push_msg_to_MSTeams,
    adaptive_card_build_MSteams,
    generate_OTP,
    verify_OTP,
    system_env_get_cred,
    login_status_check,
    logout_render,
    request_to_automate_button
)
from Activity.umc_actions import (
    login_to_site,
    add_homesis_homesis_user,
    deactivate_user_with_reason,
    sales_reactivate,
    remove_single_role,
    roles_table,
    deactivate_ra,
    check_account_status,
    add_role_umc,
    remove_multi_roles_umc,
    update_phone_number,
    update_name,
    update_dob,
    update_gender,
    update_employed_since,
    update_mail,
    reactivate_account
)
import Common.constant.app_message as app_msg
import pandas as pd
import streamlit as st

# This is to jump the user back to login if their are not authenticated
login_status_check()
logout_render()
request_to_automate_button()


def main():
    # Title of the page
    st.title("UMC AUTOMATION HUB")
    """
    This script is used for automating user account activation, deactivation, and reactivation in UMC (User Management Console).
    It utilizes the Streamlit library for creating a user interface and Selenium for interacting with the UMC web application.
    The script allows the user to input LDAP credentials, upload a CSV file containing HR codes or login names, and perform various actions on the user accounts.
    The available actions include activating accounts, deactivating accounts with a chosen reason, and reactivating accounts.
    """
    # Username & Password Input
    ldap_user = st.text_input("LDAP USERNAME")
    ldap_pw = st.text_input("LDAP PASSWORD", type="password")

    # Choose action to take on UMC
    st.subheader("Choose your action on UMC", divider="red")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Deactivate/Reactive", "Add/Remove Role", "Check status", "Update Info", "Reactivate Accounts", "Emergency Role Add"])

    with tab1:
        tab1_exec(ldap_user, ldap_pw)
    with tab2:
        tab2_exec(ldap_user, ldap_pw)
    with tab3:
        tab3_exec(ldap_user, ldap_pw)
    with tab4:
        tab4_exec(ldap_user, ldap_pw)
    with tab5:
        tab5_exec()
    with tab6:
        tab6_exec()
    pass


def tab1_exec(ldap_user: str, ldap_pw: str):
    """tab1_exec execute Deactivate LDAP account

        Args:
            username (str): str value of login name
            password (str): str value of password
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
        st.write(csv_data)

    # Activate Account

    if active_account_button:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            # Start Selenium
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
            # Loop through CSV & Search for HR Code
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                add_homesis_homesis_user(umc_page=umc_page, hr_code=hr_code)
                umc_page.get_umc_url()
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    # Deactivate Account
    if remove_roles_button:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
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
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    # Reactivate Account
    if reactivate_account_button:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            # Start Selenium
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

            # Loop through CSV & Search for HR Code
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                reason = options[options.index(deact_reason)]
                sales_reactivate(umc_page=umc_page, hr_code=hr_code)
                umc_page.get_umc_url()
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    if remove_dismissal_button:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            # Start Selenium
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

            # Loop through CSV & Search for HR Code
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                role = roles_table[options.index(deact_reason)]
                remove_single_role(umc_page=umc_page,
                                   hr_code=hr_code, role=role)
                umc_page.get_umc_url()
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    st.divider()
    st.text("Deactive RA")
    deactive_ra_button = st.button(
        "Deactive RA", type="primary")

    # deactive account
    if deactive_ra_button:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            # Start Selenium
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

            # Loop through CSV & Search for HR Code
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                deactivate_ra(umc_page=umc_page, hr_code=hr_code)
                umc_page.get_umc_url()
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)


def tab2_exec(ldap_user: str, ldap_pw: str):

    st.subheader("Add role for multiple user")
    left, rigth = st.columns(2, vertical_alignment="top")
    login_name_input_area = left.text_area("Input login name here")
    login_name_input_area_list = login_name_input_area.split(
        "\n")  # This return a list
    role_umc_input_area = rigth.text_area("Input roles here")
    role_umc_input_area_list = role_umc_input_area.split(
        "\n")  # This return a list
    add_role_umc_btn = st.button("Add roles UMC", type="primary")

    if add_role_umc_btn:
        # Start Selenium
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

            for index in range(len(login_name_input_area_list)):
                login_name = login_name_input_area_list[index]
                add_role_umc(
                    umc_page=umc_page,
                    hr_code=login_name,
                    role_list=role_umc_input_area_list,
                )
                umc_page.get_umc_url()
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    st.divider()
    st.subheader("Remove role for multiple user")
    left, rigth = st.columns(2, vertical_alignment="top")
    login_name_input_area = left.text_area("Input login name to remove here")
    login_name_input_area_list = login_name_input_area.split(
        "\n")  # This return a list
    role_umc_input_area = rigth.text_area("Input remove roles here")
    role_umc_input_area_list = role_umc_input_area.split(
        "\n")  # This return a list
    remove_role_umc_btn = st.button("Remove roles UMC", type="primary")

    if remove_role_umc_btn:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            # Start Selenium
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

            for index in range(len(login_name_input_area_list)):
                login_name = login_name_input_area_list[index]
                remove_multi_roles_umc(
                    umc_page=umc_page,
                    hr_code=login_name,
                    role_list=role_umc_input_area_list,
                )

                umc_page.get_umc_url()
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)


def tab3_exec(ldap_user: str, ldap_pw: str):
    # check active account UMC
    st.text("Check status account UMC")
    hr_code_input_area = st.text_area("Input Hr code or HCG here")
    hr_code_input_area_lines = hr_code_input_area.split(
        "\n"
    )  # This return a list of text area value
    check_status_btn = st.button("Check status account", type="primary")

    if check_status_btn:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            # Start Selenium
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
            data_user_status_list = []
            # Initial dataframe saving user status
            for hr_code in hr_code_input_area_lines:
                status = check_account_status(
                    umc_page=umc_page, hr_code=hr_code)
                data_user_status_list.append(
                    {"Hr Code": hr_code, "Status": status})  # Add to the list
                umc_page.get_umc_url()  # Move outside the loop if it doesn't depend on hr_code
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

        # Create the DataFrame *outside* the loop (only once):
        # <--- DataFrame created here
        data_user_status = pd.DataFrame(data_user_status_list)

        # display result
        left, rigth = st.columns(2, vertical_alignment="top")
        left.subheader(":red[Total result]")
        left.text("Successfully run " +
                  str(len(hr_code_input_area_lines)) + " users")
        left.write(data_user_status)
        data_user_status_inactive = data_user_status[
            data_user_status["Status"] == "Inactive"
        ]
        rigth.subheader(":red[Inactive user]")
        rigth.write(data_user_status_inactive)


def tab4_exec(ldap_user: str, ldap_pw: str):
    # List HR Code/Login Name Input
    csv_upload = st.file_uploader(
        label="HR Code/Login Name List",
        type=["csv", "txt"],
        accept_multiple_files=False,
    )
    # Read CSV Data
    if csv_upload is not None:
        csv_data = pd.read_csv(csv_upload, converters={
                               "HR Code": str, "Phone": str})
        st.write(csv_data)

    # Create columns for update UMC info
    col_1, col_2, col_3, col_4 = st.columns(4)

    # Phone Button on the Column 1
    update_phone_button = col_1.button("Update phone")
    update_employed_since_button = col_1.button("Update employed_since")

    # DoB update Button on Column 2
    update_dob_button = col_2.button("Update BoB")
    update_mail_button = col_2.button("Update Mail")

    # Update number on Column 3
    update_name_button = col_3.button("Update name")

    # Update Gender on column 4
    update_gender_button = col_4.button("Update Gender")

    # Update info account UMC
    if update_phone_button:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            # Start Selenium
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
            table_of_error = pd.DataFrame(columns=["Hr Code", "Steps"])
            left, right = st.columns(
                [0.4, 0.6], vertical_alignment="top", gap="large")
            # Loop through CSV & Search for HR Code
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                phone_number = row["Phone"]
                list_error = update_phone_number(
                    umc_page=umc_page,
                    hr_code=hr_code,
                    phone_number=phone_number
                )
                # Keep this line for debugging, but it might print None
                left.write(list_error)
                for i in range(len(list_error)):
                    table_of_error.loc[len(table_of_error)] = [
                        hr_code, list_error[i].split("-", 1)[1]]
                umc_page.get_umc_url()
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    if update_name_button:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            # Start Selenium
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
            table_of_error = pd.DataFrame(columns=["Hr Code", "Steps"])
            left, right = st.columns(
                [0.4, 0.6], vertical_alignment="top", gap="large")
            # loop through CSV & Search for HR code
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                first_name = row["First Name"]
                last_name = row["Last Name"]
                list_error = update_name(
                    umc_page=umc_page,
                    hr_code=hr_code,
                    first_name=first_name,
                    last_name=last_name
                )
                # Keep this line for debugging, but it might print None
                left.write(list_error)
                for i in range(len(list_error)):
                    table_of_error.loc[len(table_of_error)] = [
                        hr_code, list_error[i].split("-", 1)[1]]
                umc_page.get_umc_url()
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    if update_dob_button:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            # Start Selenium
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
            table_of_error = pd.DataFrame(columns=["Hr Code", "Steps"])
            left, right = st.columns(
                [0.4, 0.6], vertical_alignment="top", gap="large")
            # loop through CSV & Search for HR code
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                date_of_birth = row["DateOfBirth"]
                list_error = update_dob(
                    umc_page=umc_page,
                    hr_code=hr_code,
                    date_of_birth=date_of_birth
                )
                # Keep this line for debugging, but it might print None
                left.write(list_error)
                for i in range(len(list_error)):
                    table_of_error.loc[len(table_of_error)] = [
                        hr_code, list_error[i].split("-", 1)[1]]
                umc_page.get_umc_url()
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    if update_gender_button:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            # Start Selenium
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
            table_of_error = pd.DataFrame(columns=["Hr Code", "Steps"])
            left, right = st.columns(
                [0.4, 0.6], vertical_alignment="top", gap="large")
            # loop through CSV & Search for HR code
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                detail_gender = row["Gender"]
                list_error = update_gender(
                    umc_page=umc_page,
                    hr_code=hr_code,
                    detail_gender=detail_gender
                )
                # Keep this line for debugging, but it might print None
                left.write(list_error)
                for i in range(len(list_error)):
                    table_of_error.loc[len(table_of_error)] = [
                        hr_code, list_error[i].split("-", 1)[1]]
                umc_page.get_umc_url()
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    if update_employed_since_button:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            # Start Selenium
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
            table_of_error = pd.DataFrame(columns=["Hr Code", "Steps"])
            left, right = st.columns(
                [0.4, 0.6], vertical_alignment="top", gap="large")
            # loop through CSV & Search for HR code
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                employedSince = row["Employed Since"]
                list_error = update_employed_since(
                    umc_page=umc_page,
                    hr_code=hr_code,
                    employedSince=employedSince
                )
                # Keep this line for debugging, but it might print None
                left.write(list_error)
                for i in range(len(list_error)):
                    table_of_error.loc[len(table_of_error)] = [
                        hr_code, list_error[i].split("-", 1)[1]]
                umc_page.get_umc_url()
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    if update_mail_button:
        with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
            # Start Selenium
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
            table_of_error = pd.DataFrame(columns=["Hr Code", "Steps"])
            left, right = st.columns(
                [0.4, 0.6], vertical_alignment="top", gap="large")
            # loop through CSV & Search for HR code
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                mail = row["Mail"]
                list_error = update_mail(
                    umc_page=umc_page,
                    hr_code=hr_code,
                    mail=mail
                )
                # Keep this line for debugging, but it might print None
                left.write(list_error)
                for i in range(len(list_error)):
                    table_of_error.loc[len(table_of_error)] = [
                        hr_code, list_error[i].split("-", 1)[1]]
                umc_page.get_umc_url()
        st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)


def tab5_exec():
    st.subheader("Reactivate accounts on UMC")

    login_name_input_area = st.text_area("Please insert reactive account here")
    login_name_input_area_list = login_name_input_area.split(
        "\n")  # This return a list

    if login_name_input_area != '':

        # Show 5 rows of data on screen
        # data = pd.read_csv(reactivate_upload, converters={"HRcode": str})
        # st.subheader(
        #     "First 5 rows", help="Please check the HR Code to make sure you are running the correct file")
        # st.write(data.head(5))
        # Initialize Session State to properly perform nested button
        if 'getOTP_clicked' not in st.session_state:
            st.session_state['getOTP_clicked'] = False
        if 'confirmOTP_clicked' not in st.session_state:
            st.session_state['confirmOTP_clicked'] = False
        if 'timeOTP' not in st.session_state:
            st.session_state['timeOTP'] = None

        # Building FrontEnd Button to get OTP
        getOTP = st.button("Get OTP", use_container_width=True)
        if getOTP:
            st.session_state['getOTP_clicked'] = True

        if st.session_state['getOTP_clicked'] and getOTP:
            # Trigger OTP Generation
            st.session_state['timeOTP'] = generate_OTP()

        # Display OTP verification input if OTP was generated
        if st.session_state['getOTP_clicked']:
            # Building FrontEnd OTP Verification
            col1, col2 = st.columns([1, 2], vertical_alignment="bottom")
            with col1:
                OTP = st.text_input("Verify OTP")
            with col2:
                confirm = st.button("Confirm OTP")
            if confirm:
                st.session_state['confirmOTP_clicked'] = True
                result = verify_OTP(
                    sourceOTP=st.session_state['timeOTP'], OTP=OTP)
                if not result:
                    st.write("OTP failed to verify!")

                    # Reset session state after function complete
                    st.session_state.clear()

            # Run Reactivate Scripts if the verification returns valid
            if st.session_state['confirmOTP_clicked'] and result is True:
                with st.spinner('Processing...'):
                    from time import sleep
                    # Trigger request to CBA Vault to get UMC password
                    cred = system_env_get_cred()
                    sleep(5)
                    umc_page = login_to_site(
                        ldap_user="umc_admin1", ldap_pw=cred)
                    # table_of_error = pd.DataFrame(columns=["Hr Code", "Steps"])
                    # log_left, log_right = st.columns([0.4, 0.6], vertical_alignment="top", gap="large")
                    for index, hr_code in enumerate(login_name_input_area_list):
                        reactivation_status = reactivate_account(
                            umc_page=umc_page, hr_code=hr_code)
                        if reactivation_status is False:
                            st.write(hr_code + ": Reactivation Failed")
                        umc_page.get_umc_url()
                    # Reset session state after function complete
                    st.session_state.clear()


def tab6_exec():
    st.subheader("Emergency add role on UMC")

    hr_code_text_area = st.text_area("Input Hr codes or HCGs")
    if hr_code_text_area is not None:
        hr_code_input_area_lines = hr_code_text_area.split(
            "\n"
        )
        emergency = st.button("Perform emergency add role", type="primary")
        if emergency:
            with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
                cred = system_env_get_cred()
                umc_page = login_to_site(ldap_user="umc_admin1", ldap_pw=cred)
                for code in hr_code_input_area_lines:
                    add_role_status = add_role_umc(
                        umc_page=umc_page, hr_code=code, role_list=["NON_HOSEL_USER"])
                    if add_role_status is False:
                        st.write(code + ": Emergency add role Failed")
                    umc_page.get_umc_url()
            st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)


if __name__ == "__main__":
    main()
