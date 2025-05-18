import time
import streamlit as st
import pandas as pd


from Activity.idm_actions import (
    login_to_site,
    search_user_by_login_name,
    access_user_profile,
    get_user_info,
    search_user_in_modify,
    search_user_by_hr_code

)


def main():

    st.title("IDM Automation")
    st.text("Extract data from IDM in user")
    st.divider()
    right_col, left_col = st.columns([4, 6])
    data_extract_options = ["User Hr Code", "User Login Name", "User Email", "User Job Position",
                            "User Organization", "User Manager Account", "User Status"]
    user_type_of_information_search = [
        "Search by Hr Code", "Search by Login Name", "Search user's manager account"]
    idm_login_name_input_area = right_col.text_area(
        "Input IDM login here", height=350)
    idm_login_name_input_list = idm_login_name_input_area.split(
        "\n")  # This return a list

# Get current selections
    selected_user_type_of_information = left_col.selectbox(
        "Select the type of search and choose the info you wanna extract", user_type_of_information_search)

    if selected_user_type_of_information == "Search user's manager account":
        data_extract_options = ["User's Manager Account"]

    selected_options = [
        opt for opt in data_extract_options if left_col.checkbox(opt)]

    user_data = {option: [] for option in selected_options}

    # Inject CSS to customize button width
    st.markdown(
        """
        <style>
        /* Make all buttons wider */
        div.stButton > button {
            width: 100%;
            height: 10%;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    test_button = st.button("Extract button", type="primary")

    if test_button:
        idm_page = login_to_site()
        time.sleep(15)
        idm_page.click_user_tab()
        time.sleep(1)
        idm_page.click_manage_user()
        for login_name in idm_login_name_input_list:
            if selected_user_type_of_information == "Search user's manager account":
                if "User's Manager Account" in selected_options:
                    idm_page.click_view_user_modify()
                    search_user_in_modify(
                        idm_page=idm_page, user_login_name=login_name)
                    time.sleep(0.5)
                    access_user_profile(idm_page=idm_page)
                    try:
                        user_manager_account = get_user_info(
                            idm_page=idm_page, element_id="idmCustomAttribute26")
                        user_data["User's Manager Account"].append(
                            user_manager_account)
                    except Exception:
                        user_data["User's Manager Account"].append(None)

            if selected_user_type_of_information == "Search by Login Name":
                search_user_by_login_name(
                    idm_page=idm_page, user_login_name=login_name)

            if selected_user_type_of_information == "Search by Hr Code":
                search_user_by_hr_code(
                    idm_page=idm_page, user_login_name=login_name)

                if "User Hr Code" in selected_options:
                    try:
                        time.sleep(1)
                        user_hr_code = idm_page.get_user_hr_code()

                        user_data["User Hr Code"].append(user_hr_code)
                    except Exception:
                        user_data["User Hr Code"].append(None)

                if "User Login Name" in selected_options:
                    try:
                        time.sleep(1)
                        user_login_name = idm_page.get_user_login_name()

                        user_data["User Login Name"].append(user_login_name)
                    except Exception:
                        user_data["User Login Name"].append(None)

                if "User Status" in selected_options:
                    try:
                        time.sleep(1)
                        user_status = idm_page.get_user_status()
                        user_data["User Status"].append(user_status)
                    except Exception:
                        user_data["User Status"].append(None)

                if "User Email" in selected_options:
                    try:
                        time.sleep(1)
                        user_email = idm_page.get_user_email()
                        user_data["User Email"].append(user_email)
                    except Exception:
                        user_data["User Email"].append(None)

                if "User Job Position" in selected_options:
                    try:
                        time.sleep(1)
                        user_job_position = idm_page.get_user_position()
                        user_data["User Job Position"].append(
                            user_job_position)
                    except Exception:
                        user_data["User Job Position"].append(None)

                if "User Organization" in selected_options:
                    try:
                        time.sleep(1)
                        user_organization = idm_page.get_user_organization()
                        user_data["User Organization"].append(
                            user_organization)
                    except Exception:
                        user_data["User Organization"].append(None)

                idm_page.get_idm_url()
                idm_page.click_login_button()

    st.text("The Result Table")
    df = pd.DataFrame(user_data)
    st.dataframe(df)


if __name__ == "__main__":
    main()
