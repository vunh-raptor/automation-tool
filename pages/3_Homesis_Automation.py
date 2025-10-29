import streamlit as st
from Common.constant import exception

# This is to jump the user back to login if their are not authenticated
if st.session_state["authenticated"] is not True:
    st.switch_page("main_site.py")

import pandas as pd
from Common.constant.css_file import css
import Common.constant.app_message as app_msg
from Common.constant import app_logic_exception


from Activity.homesis_actions import (
    login_to_site,
    add_role_in_bank_RA_MW,
    add_role_in_bank_SA,
    add_role_in_bank_RA_FPT,
    add_role_in_bank_RA_New_Segment,
    change_role_in_bank,
    add_sup_code,
    update_note,
    update_id_number,
    closed_partner,
)

from Common.supporting import (
    login_status_check,
    logout_render
)

# This is to jump the user back to login if their are not authenticated
login_status_check()
logout_render()


@app_logic_exception.app_logic_exception_handler
def main():
    """
    This function is to support SD task interact with Homesis
    """
    # Title of the page
    homesis_page_title = st.title("HOMESIS AUTOMATION HUB")

    # Username & Password Input
    ldap_user = st.text_input("Homesis Username")
    ldap_pw = st.text_input("Password", type="password")

    # Insert excel file for create Homesis account
    csv_upload_homesis_template = st.file_uploader(
        label="Please input Homesis_Role_In_Bank_Template.csv. You can find it here",
        type=["csv", "txt"],
        accept_multiple_files=False,
    )

    # Read CSV Data
    if csv_upload_homesis_template is not None:
        csv_data = pd.read_csv(
            csv_upload_homesis_template,
            converters={
                "HR Code": str,
                "ID number": str,
                "Supervisor code": str,
                "Notes": str,
                "Role in Bank": str,
                "Location": str,
            },
        )
        result_table = st.write(csv_data)

    # Chose action on Homesis page
    section_divided_caption = st.header("Please chose your action")

    # Chose action on Homesis page
    section_divided_caption = st.subheader("Add role in bank", divider="red")

    tab1, tab2, tab3, tab4 = st.tabs(["SA Home", "RA MW", "RA FPT", "RA NS"])
    with tab1:
        st.markdown("Required field:")
        st.text("HR Code, ID number, Notes, Sup Code, Role SA, Location")
        # Add role in bank SA button
        add_role_in_bank_SA_btn = st.button(
            "Add role-in-bank SA", type="primary")
        # Add role in bank SA for Homesis page
        if add_role_in_bank_SA_btn:
            with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
                # Start Selenium
                homesis_page = login_to_site(
                    ldap_user=ldap_user, ldap_pw=ldap_pw)
                homesis_page.access_user_managerment()
                table_of_error = pd.DataFrame(columns=["Hr Code", "Steps"])
                left, rigth = st.columns(
                    [0.4, 0.6], vertical_alignment="top", gap="large")
                # Loop through CSV & Search for HR Code and take data from CSV
                for index, row in csv_data.iterrows():
                    hr_code = row["HR Code"]
                    id_number = row["ID number"]
                    note = row["Notes"]
                    supervisor = row["Supervisor code"]
                    role = row["Role in Bank"]
                    location = row["Location"]
                    list_error = add_role_in_bank_SA(
                        homesis_page=homesis_page,
                        hr_code=hr_code,
                        id_number=id_number,
                        note=note,
                        supervisor_code=supervisor,
                        role=role,
                        location=location,
                    )
                    left.write(list_error)
                    for i in range(len(list_error)):
                        table_of_error.loc[len(table_of_error)] = [
                            hr_code, list_error[i].split("-", 1)[1]]

                    homesis_page.get_homesis_url()
                    homesis_page.access_user_managerment()
                rigth.write("Run through " +
                            str(csv_data.__len__()) + " users")
                rigth.subheader("List of errors")
                rigth.write(
                    table_of_error.loc[
                        table_of_error["Steps"]
                        != " Click Save button successfully"
                    ]
                )
            st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    with tab2:
        st.markdown("Required field:")
        st.text("HR Code, Notes, Role RA")

        # Add role in bank RA MW button
        add_role_in_bank_RA_MW_btn = st.button(
            "Add role-in-bank RA MW", type="primary")
        # Add role in bank RA MW for Homesis page
        if add_role_in_bank_RA_MW_btn:
            with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
                # Start Selenium
                homesis_page = login_to_site(
                    ldap_user=ldap_user, ldap_pw=ldap_pw)
                homesis_page.access_user_managerment()
                table_of_error = pd.DataFrame(columns=["Hr Code", "Steps"])
                left, rigth = st.columns(
                    [0.4, 0.6], vertical_alignment="top", gap="large")
                # Loop through CSV & Search for HR Code and take data from CSV
                for index, row in csv_data.iterrows():
                    hr_code = row["HR Code"]
                    note = row["Notes"]
                    role = row["Role in Bank"]
                    list_of_error = add_role_in_bank_RA_MW(
                        homesis_page=homesis_page,
                        hr_code=hr_code,
                        note=note,
                        role=role,
                    )
                    left.write(list_of_error)
                    for i in range(len(list_of_error)):
                        table_of_error = table_of_error.append(
                            {"Hr Code": hr_code,
                                "Steps": list_of_error[i].split("-", 1)[1]},
                            ignore_index=True,
                        )
                    homesis_page.get_homesis_url()
                    homesis_page.access_user_managerment()
                rigth.write("Run through " +
                            str(csv_data.__len__()) + " users")
                rigth.subheader("List of errors")
                rigth.write(
                    table_of_error.loc[
                        table_of_error["Steps"]
                        != " Click Save button successfully"
                    ]
                )
            st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    with tab3:
        st.markdown("Required field:")
        st.text("HR Code, Notes, Role RA, ID number")
        # Add role in bank RA FPT button
        add_role_in_bank_RA_FPT_btn = st.button(
            "Add role-in-bank RA FPT", type="primary"
        )
        # Add role in bank RA FPT for Homesis page
        if add_role_in_bank_RA_FPT_btn:
            with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
                # Start Selenium
                homesis_page = login_to_site(
                    ldap_user=ldap_user, ldap_pw=ldap_pw)
                homesis_page.access_user_managerment()
                table_of_error = pd.DataFrame(columns=["Hr Code", "Steps"])
                left, rigth = st.columns(
                    [0.4, 0.6], vertical_alignment="top", gap="large")
                # Loop through CSV & Search for HR Code and take data from CSV
                for index, row in csv_data.iterrows():
                    hr_code = row["HR Code"]
                    id_number = row["ID number"]
                    note = row["Notes"]
                    role = row["Role in Bank"]
                    list_error = add_role_in_bank_RA_FPT(
                        homesis_page=homesis_page,
                        hr_code=hr_code,
                        id_number=id_number,
                        note=note,
                        role=role,
                    )
                    left.write(list_error)
                    for i in range(len(list_error)):
                        table_of_error = table_of_error._append(
                            {"Hr Code": hr_code,
                                "Steps": list_error[i].split("-", 1)[1]},
                            ignore_index=True,
                        )
                    homesis_page.get_homesis_url()
                    homesis_page.access_user_managerment()
                rigth.write("Run through " +
                            str(csv_data.__len__()) + " users")
                rigth.subheader("List of errors")
                rigth.write(
                    table_of_error.loc[
                        table_of_error["Steps"]
                        != " Click Save button successfully"
                    ]
                )
            st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    with tab4:
        st.markdown("Required field:")
        st.text("HR Code, Notes, Role RA, ID number, Sup Code")
        # Add role in bank RA button
        add_role_in_bank_RA_NS_btn = st.button(
            "Add role-in-bank RA New Segment", type="primary"
        )
        # Add role in bank RA New Segment for Homesis page
        if add_role_in_bank_RA_NS_btn:
            with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
                # Start Selenium
                homesis_page = login_to_site(
                    ldap_user=ldap_user, ldap_pw=ldap_pw)
                homesis_page.access_user_managerment()
                table_of_error = pd.DataFrame(columns=["Hr Code", "Steps"])
                left, rigth = st.columns(
                    [0.4, 0.6], vertical_alignment="top", gap="large")
                # Loop through CSV & Search for HR Code and take data from CSV
                for index, row in csv_data.iterrows():
                    hr_code = row["HR Code"]
                    id_number = row["ID number"]
                    note = row["Notes"]
                    role = row["Role in Bank"]
                    supervisor = row["Supervisor code"]
                    list_error = add_role_in_bank_RA_New_Segment(
                        homesis_page=homesis_page,
                        hr_code=hr_code,
                        id_number=id_number,
                        note=note,
                        role=role,
                        supervisor_code=supervisor,
                    )
                    left.write(list_error)
                    for i in range(len(list_error)):
                        table_of_error = table_of_error._append(
                            {"Hr Code": hr_code,
                                "Steps": list_error[i].split("-", 1)[1]},
                            ignore_index=True,
                        )
                    homesis_page.get_homesis_url()
                    homesis_page.access_user_managerment()
                rigth.write("Run through " +
                            str(csv_data.__len__()) + " users")
                rigth.subheader("List of errors")
                rigth.write(
                    table_of_error.loc[
                        table_of_error["Steps"]
                        != " Click Save button successfully"
                    ]
                )
            st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    section_divided_caption_other_action = st.subheader(
        "Update Homesis information", divider="red"
    )

    (
        change_role_in_bank_tab,
        add_sup_code_tab,
        update_note_tab,
        update_id_number_tab,
        other,
    ) = st.tabs(
        [
            "Change Role-in-bank",
            "Add sup code",
            "Update Note",
            "Update ID number",
            "Other",
        ]
    )

    with change_role_in_bank_tab:
        left, rigth = st.columns(2, vertical_alignment="bottom")

        # Upload list Hr code
        csv_upload_hrcode_change_role_in_bank = left.file_uploader(
            label="Please input list of HR code you want to change role in bank",
            type=["csv", "txt"],
            accept_multiple_files=False,
        )
        # Read CSV Data
        if csv_upload_hrcode_change_role_in_bank is not None:
            csv_data_change_role_in_bank = pd.read_csv(
                csv_upload_hrcode_change_role_in_bank, converters={
                    "HR Code": str}
            )

        # Select the option for change the role in bank
        option = rigth.selectbox(
            "Chose a role-in-bank",
            ("** choose **",
             "SA",
             "RA",
             "DSM",
             "KA",
             "SDSM",
             "RSMA",
             "RSM",
             "Admin - specialist",
             "Admin - supervisor",
             "Admin - manager",
             "Director of Sales // CEO",
             "Risk",
             "Security",
             "VNPOST(OP)",
             "BD DSM",
             "Other",
             "BD SA",
             "Area sales manager",
             "Regional Key Account Manager",
             "Sales Agent Online",
             "Tipper",
             "Telesales operator",
             "Telesales operator - push sevice",
             "Telesales Call Center Team Leader",
             "Telesales Call Center Supervisor",
             "Telesales Call Center Quality Controller",
             "Telesales Call Center Manager"),
            index=None,
        )

        # Input css for upload file in change role in bank section
        st.markdown(css.css, unsafe_allow_html=True)

        # Change role in bank button
        change_role_in_bank_btn = st.button(
            "Change Role-in-Bank", type="primary")
        # Change role in bank action
        if change_role_in_bank_btn:
            with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
                # Start Selenium
                homesis_page = login_to_site(
                    ldap_user=ldap_user, ldap_pw=ldap_pw)
                homesis_page.access_user_managerment()

                # Loop through CSV & Search for HR Code and take data from CSV
                for index, row in csv_data_change_role_in_bank.iterrows():
                    hr_code = row["HR Code"]
                    role = option
                    change_role_in_bank(
                        homesis_page=homesis_page, hr_code=hr_code, role=option
                    )
                    homesis_page.get_homesis_url()
                    homesis_page.access_user_managerment()
            st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    with add_sup_code_tab:
        st.text(
            ":red[Please make sure these user are not assign any sup code before]")
        # Insert excel file for add sup code
        csv_upload_homesis_add_sup_code = st.file_uploader(
            label="Please input list user and their sup code",
            type=["csv", "txt"],
            accept_multiple_files=False,
        )

        # Read CSV Data
        if csv_upload_homesis_add_sup_code is not None:
            csv_data_add_sup_code = pd.read_csv(
                csv_upload_homesis_add_sup_code,
                converters={"HR Code": str, "Supervisor code": str},
            )
            result_table = st.write(csv_data_add_sup_code)

        # nhét chức năng thêm dô ở đây
        add_sup_code_btn = st.button("Add Sup Code", type="primary")
        if add_sup_code_btn:
            with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
                # Start Selenium
                homesis_page = login_to_site(
                    ldap_user=ldap_user, ldap_pw=ldap_pw)
                homesis_page.access_user_managerment()

                # Loop through CSV & Search for HR Code and take data from CSV
                for index, row in csv_data_add_sup_code.iterrows():
                    hr_code = row["HR Code"]
                    supervisor = row["Supervisor code"]
                    list_error = add_sup_code(
                        homesis_page=homesis_page,
                        hr_code=hr_code,
                        supervisor_code=supervisor,
                    )
                    st.write(list_error)
                    homesis_page.get_homesis_url()
                    homesis_page.access_user_managerment()
            st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    with update_note_tab:
        # Insert excel file for create Homesis account
        csv_upload_homesis_update_note = st.file_uploader(
            label="Please input list user and their note update",
            type=["csv", "txt"],
            accept_multiple_files=False,
        )

        # Read CSV Data
        if csv_upload_homesis_update_note is not None:
            csv_data_update_note = pd.read_csv(
                csv_upload_homesis_update_note, converters={
                    "HR Code": str, "Note": str}
            )
            result_table = st.write(csv_data_update_note)

        # nhét chức năng thêm dô ở đây
        update_note_btn = st.button("Update Note", type="primary")
        if update_note_btn:
            with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
                # Start Selenium
                homesis_page = login_to_site(
                    ldap_user=ldap_user, ldap_pw=ldap_pw)
                homesis_page.access_user_managerment()

                # Loop through CSV & Search for HR Code and take data from CSV
                for index, row in csv_data_update_note.iterrows():
                    hr_code = row["HR Code"]
                    note = row["Notes"]
                    update_note(homesis_page=homesis_page,
                                hr_code=hr_code, note=note)
                    homesis_page.get_homesis_url()
                    homesis_page.access_user_managerment()
            st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    with update_id_number_tab:
        # Insert excel file for create Homesis account
        csv_upload_homesis_update_id_number = st.file_uploader(
            label="Please input list user and their ID number update",
            type=["csv", "txt"],
            accept_multiple_files=False,
        )

        # Read CSV Data
        if csv_upload_homesis_update_id_number is not None:
            csv_data_update_id_number = pd.read_csv(
                csv_upload_homesis_update_id_number,
                converters={"HR Code": str, "ID number": str},
            )
            result_table = st.write(csv_data_update_id_number)

        # function to update ID number
        update_id_number_btn = st.button("Update ID number", type="primary")
        if update_id_number_btn:
            with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
                # Start Selenium
                homesis_page = login_to_site(
                    ldap_user=ldap_user, ldap_pw=ldap_pw)
                homesis_page.access_user_managerment()

                # Loop through CSV & Search for HR Code and take data from CSV
                for index, row in csv_data_update_id_number.iterrows():
                    hr_code = row["HR Code"]
                    id_number = row["ID number"]
                    update_id_number(
                        homesis_page=homesis_page, hr_code=hr_code, id_number=id_number
                    )
                    homesis_page.get_homesis_url()
                    homesis_page.access_user_managerment()
            st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    section_divided_caption_other_action = st.subheader(
        "Close/Block Shopcode/Partner", divider="red"
    )

    (
        partner_tab,
        shopcode_tab,
    ) = st.tabs(
        [
            "PARTNER",
            "SHOPCODE",

        ]
    )

    with partner_tab:
        text = "This action may have consequence, please carefully check your data before click execute button."
        st.markdown(
            f"<div style='color: red; word-wrap: break-word;'>{text}</div>", unsafe_allow_html=True)

        partner_codes_input_area = st.text_area("Input partner codes here")
        partner_codes_input_area_list = partner_codes_input_area.split(
            "\n")  # This return a list of partner code
        filtered_list = list(filter(None, partner_codes_input_area_list))
        clean_value_partner_codes_input_area_list = [
            item.strip() for item in filtered_list]

        option = st.selectbox(
            "Choose action with partner",
            ("Closed", "Blocked"),
            index=None,
        )

        if option == "Closed" and partner_codes_input_area != '':
            execute_action_with_btn = st.button(
                "Execute action with partners", type="primary")

            if execute_action_with_btn:
                with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
                    # Start Selenium
                    homesis_page = login_to_site(
                        ldap_user=ldap_user, ldap_pw=ldap_pw)
                    homesis_page.access_sales_managerment()
                    count = 0
                    if option == "Closed":
                        for index, partner_code in enumerate(clean_value_partner_codes_input_area_list):

                            if len(partner_code) == 6:
                                count += 1
                                closed_partner(homesis_page=homesis_page,
                                               partner_code=partner_code)

                                homesis_page.get_homesis_url()
                                homesis_page.access_sales_managerment()
                            else:
                                st.write("Code này khác 6 kí tự - " +
                                         str(partner_code))

                        st.write("Tool đã đóng " +
                                 str(count) + " partner code.")
                st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

        if option == "Blocked":
            st.text("This action is not available")

    with shopcode_tab:
        text = "This feature remains in its testing phase. Due to the potential for significant adverse impacts, it is currently unavailable."
        st.markdown(
            f"<div style='color: red; word-wrap: break-word;'>{text}</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
