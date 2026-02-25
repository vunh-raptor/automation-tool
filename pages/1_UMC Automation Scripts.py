from Common.supporting import (
    push_msg_to_MSTeams,
    adaptive_card_build_MSteams,
    generate_OTP,
    verify_OTP,
    system_env_get_cred,
    login_status_check,
    logout_render,
    authenticate_swagger,
    authenticate_HOSELSSO,
    request_to_automate_button
)
from Activity.umc_actions import (
    login_to_site,
    add_homesis_homesis_user,
    deactivate_ra,
    check_account_status,
    add_role_umc,
    add_multi_role_umc,
    remove_multi_role_umc,
    update_phone_number,
    update_name,
    update_dob,
    update_gender,
    update_employed_since,
    update_mail,
    reactivate_account,
    umc_start_session,
    get_deactivation_date
)
from Common.constant.app_message import APP_MESSAGE as app_msg
import pandas as pd
import streamlit as st
from Common.constant import app_logic_exception

# This is to jump the user back to login if their are not authenticated
login_status_check()
logout_render()
request_to_automate_button()

# ------------------------------------------Helpers------------------------------------------


def authen_get_UMC_session(username: str, password: str):
    if not authenticate_HOSELSSO(username=username, password=password):
        st.error(app_msg.APP_LOGIN_FAILED_MSG)
        return None
    return umc_start_session(authenticate_swagger(username=username, password=password))


# ------------------------------------------Main------------------------------------------
@app_logic_exception.app_logic_exception_handler
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
        ["Deactivate/Reactive", "Add/Remove Role", "Check status", "Update Info", "Reactivate Accounts", "Get account deactivation date"])

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

    # List HR Code/Login Name Input
    csv_upload = st.file_uploader(
        label="HR Code/Log In Name List",
        type=["csv", "txt"],
        accept_multiple_files=False,
    )

    # Read CSV Data
    if csv_upload is not None:
        csv_data = pd.read_csv(csv_upload, converters={"HR Code": str})
        st.write(csv_data)

    st.text("Deactive RA")
    deactive_ra_button = st.button(
        "Deactive RA", type="primary")

    # deactive account
    if deactive_ra_button:
        with st.spinner(app_msg.APP_RUNNING_MSG):
            request = authen_get_UMC_session(
                username=ldap_user, password=ldap_pw)
            if request is None:
                return
            # Loop through CSV & Search for HR Code
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                if not deactivate_ra(umc_request=request, hr_code=hr_code):
                    st.write(f"Deactivation failed for account {hr_code}")
            st.write(app_msg.APP_FINISH_MSG)


def tab2_exec(ldap_user: str, ldap_pw: str):

    st.subheader("Add role for multiple user")
    left, right = st.columns(2, vertical_alignment="top")
    login_name_input_area = left.text_area("Input login name here")
    login_name_input_area_list = login_name_input_area.split(
        "\n")  # This return a list
    role_umc_input_area = right.text_area("Input roles here")
    role_umc_input_area_list = role_umc_input_area.split(
        "\n")  # This return a list
    if login_name_input_area.strip() != '' and role_umc_input_area.strip() != '':
        add_role_umc_btn = st.button("Add roles UMC", type="primary")
        if add_role_umc_btn:
            # Start Selenium
            with st.spinner(app_msg.APP_RUNNING_MSG):
                request = authen_get_UMC_session(
                    username=ldap_user, password=ldap_pw)
                if request is None:
                    return
                status = add_multi_role_umc(
                    umc_request=request, hr_codes=login_name_input_area_list, role_list=role_umc_input_area_list)
                if status:
                    st.write(" All accounts - Add role successful")
                st.write(app_msg.APP_FINISH_MSG)

    st.divider()
    st.subheader("Remove role for multiple user")
    left, right = st.columns(2, vertical_alignment="top")
    login_name_input_area1 = left.text_area("Input login name to remove here")
    login_name_input_area_list1 = login_name_input_area1.split(
        "\n")  # This return a list
    role_umc_input_area1 = right.text_area("Input remove roles here")
    role_umc_input_area_list1 = role_umc_input_area1.split(
        "\n")  # This return a list

    if login_name_input_area1.strip() != '' and role_umc_input_area1.strip() != '':
        remove_role_umc_btn = st.button("Remove roles UMC", type="primary")
        if remove_role_umc_btn:
            with st.spinner(app_msg.APP_RUNNING_MSG):
                request = authen_get_UMC_session(
                    username=ldap_user, password=ldap_pw)
                if request is None:
                    return
                status = remove_multi_role_umc(umc_request=request, hr_codes=login_name_input_area_list1, role_list=role_umc_input_area_list1)
                if status:
                    st.write(" All accounts - Remove role successful")
                st.write(app_msg.APP_FINISH_MSG)

def tab3_exec(ldap_user: str, ldap_pw: str):
    # check active account UMC
    st.text("Check status account UMC")
    hr_code_input_area = st.text_area("Input Hr code or HCG here")
    hr_code_input_area_lines = hr_code_input_area.split(
        "\n"
    )  # This return a list of text area value
    check_status_btn = st.button("Check status account", type="primary")

    if check_status_btn:
        with st.spinner(app_msg.APP_RUNNING_MSG):
            request = authen_get_UMC_session(
                username=ldap_user, password=ldap_pw)
            if request is None:
                return
            data_user_status_list = []
            for hr_code in filter(None, hr_code_input_area_lines):
                status = check_account_status(
                    umc_request=request, hr_code=hr_code)
                data_user_status_list.append(
                    {"HR Code": hr_code, "Status": status})
            st.write(app_msg.APP_FINISH_MSG)

            # Create the DataFrame *outside* the loop (only once):
            # <--- DataFrame created here
            data_user_status = pd.DataFrame(data_user_status_list)

            # display result
            left, right = st.columns(2, vertical_alignment="top")
            data_user_status_inactive = data_user_status[
                data_user_status["Status"] == "INACTIVE"
            ]
            right.divider(width="stretch")
            right.subheader(":red[Inactive user]")
            right.text(
                f"Found {len(data_user_status_inactive)} inactive user(s)")
            right.write(data_user_status_inactive)
            left.subheader(":red[Total result]")
            left.subheader(":red[Active Users]")
            left.text("Successfully run " +
                      str(len(data_user_status)) + " users")
            data_user_status = data_user_status[data_user_status["Status"] != "INACTIVE"]
            left.write(data_user_status)


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
        with st.spinner(app_msg.APP_RUNNING_MSG):
            umc_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
            table_of_error = pd.DataFrame(columns=["Hr Code", "Steps"])
            left, right = st.columns(
                [0.4, 0.6], vertical_alignment="top", gap="large")
            if umc_page is None:
                return
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                phone_number = row["Phone"]
                list_error = update_phone_number(umc_page=umc_page, hr_code=hr_code, phone_number=phone_number)
                left.write(list_error)
                for i in range(len(list_error)):
                    table_of_error.loc[len(table_of_error)] = [
                        hr_code, list_error[i].split("-", 1)[1]]
                umc_page.get_umc_url()
            st.write(app_msg.APP_FINISH_MSG)

    if update_name_button:
        with st.spinner(app_msg.APP_RUNNING_MSG):
            request = authen_get_UMC_session(
                username=ldap_user, password=ldap_pw)
            if request is None:
                return
            # loop through CSV & Search for HR code
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                first_name = row["First Name"]
                last_name = row["Last Name"]
                status = update_name(
                    umc_request=request, hr_code=hr_code, first_name=first_name, last_name=last_name)
                if not status:
                    st.write(
                        f"{hr_code} - Failed - Change information unsuccessful!")
            st.write(app_msg.APP_FINISH_MSG)

    if update_dob_button:
        with st.spinner(app_msg.APP_RUNNING_MSG):
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
                left.write(list_error)
                for i in range(len(list_error)):
                    table_of_error.loc[len(table_of_error)] = [
                        hr_code, list_error[i].split("-", 1)[1]]
                umc_page.get_umc_url()
        st.write(app_msg.APP_FINISH_MSG)

    if update_gender_button:
        with st.spinner(app_msg.APP_RUNNING_MSG):
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
        st.write(app_msg.APP_FINISH_MSG)

    if update_employed_since_button:
        with st.spinner(app_msg.APP_RUNNING_MSG):
            request = authen_get_UMC_session(
                username=ldap_user, password=ldap_pw)
            if request is None:
                return
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                employedSince = row["Employed Since"]
                status = update_employed_since(
                    umc_request=request, hr_code=hr_code, employedSince=employedSince)
                # Keep this line for debugging, but it might print None
            st.write(app_msg.APP_FINISH_MSG)

    if update_mail_button:
        with st.spinner(app_msg.APP_RUNNING_MSG):
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
        st.write(app_msg.APP_FINISH_MSG)


def tab5_exec():
    st.subheader("Reactivate accounts on UMC")

    login_name_input_area = st.text_area("Please insert reactive account here")
    login_name_input_area_list = login_name_input_area.split(
        "\n")  # This return a list

    if login_name_input_area != '':
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
                    st.session_state['getOTP_clicked'] = False
                    st.session_state['confirmOTP_clicked'] = False
                    st.rerun()

            # Run Reactivate Scripts if the verification returns valid
            if st.session_state['confirmOTP_clicked'] and result is True:
                with st.spinner(app_msg.APP_RUNNING_MSG):
                    from time import sleep
                    # Trigger request to CBA Vault to get UMC password
                    usercred = system_env_get_cred("UMCAdminUser")
                    passcred = system_env_get_cred("UMCAdminCred")
                    sleep(5)
                    request = umc_start_session(token=authenticate_swagger(
                        username=usercred, password=passcred))
                    hr_codes = []

                    for index, hr_code in enumerate(login_name_input_area_list):
                        hr_codes.append(hr_code)
                        status = reactivate_account(
                            umc_request=request, hr_code=hr_code)
                        if status:
                            st.write(f"{hr_code}: Reactivation Successful!")
                    if add_homesis_homesis_user(umc_request=request, hr_codes=hr_codes):
                        st.write(f"{hr_code}: Add HSIS Roles Successful!")
                    st.session_state['getOTP_clicked'] = False
                    st.session_state['confirmOTP_clicked'] = False
                    st.rerun()


def tab6_exec():
    st.subheader("Get account Deactivation date")

    hr_code_text_area = st.text_area("Input Hr codes or HCGs")
    if hr_code_text_area is not None:
        hr_code_input_area_lines = hr_code_text_area.split(
            "\n"
        )
        emergency = st.button("Perform emergency add role", type="primary")
        if emergency:
            with st.spinner(app_msg.APP_RUNNING_MSG):
                usercred = system_env_get_cred("UMCAdminUser")
                passcred = system_env_get_cred("UMCAdminCred")
                request = umc_start_session(authenticate_swagger(
                    username=usercred, password=passcred))
                # add_role_status = add_role_umc(
                #     umc_request=request, hr_codes=hr_code_input_area_lines, role="NON_HOSEL_USER")
                for hr_code in hr_code_input_area_lines:
                    deactivation_date = get_deactivation_date(
                        umc_request=request, hr_code=hr_code)
                    st.write(deactivation_date)
            st.write(app_msg.APP_FINISH_MSG)


if __name__ == "__main__":
    main()
