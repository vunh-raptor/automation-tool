import pandas as pd
import streamlit as st

import Common.constant.app_message as app_msg
from Common.constant import app_logic_exception
from Common.constant.error_message import ErrorMessage
from Common.supporting import login_status_check, logout_render, authenticate_swagger

from Activity.umc_actions import (
    login_to_site as login_to_umc_site,
    umc_start_session,
    update_dob,
    update_gender,
    update_name,
    add_multi_role_umc,
    remove_multi_role_umc,
)
from Activity.homesis_actions import (
    login_to_site as login_to_homesis_site,
    add_role_in_bank_SA,
    remove_role_in_bank_SA,
)


login_status_check()
logout_render()

REQUIRED_COLUMNS = [
    "HR Code",
    "ID number",
    "Notes",
    "Supervisor code",
    "Role in Bank",
    "Location",
    "DateOfBirth",
    "Gender",
    "First Name",
    "Last Name",
]


@app_logic_exception.app_logic_exception_handler
def main():
    st.title("UMC + HOMESIS CROSS AUTOMATION")
    st.caption(
        "Upload SA Home template columns and append: First Name, Last Name, DateOfBirth, Gender."
    )

    left_col, right_col = st.columns(2)
    with left_col:
        st.subheader("Homesis Login")
        ldap_user = st.text_input("LDAP Username")
        ldap_pw = st.text_input("LDAP Password", type="password")

    with right_col:
        st.subheader("UMC Technical Login")
        technical_user = st.text_input("Technical Username")
        technical_pw = st.text_input("Technical Password", type="password")

    tab_update, tab_deactivate = st.tabs([
        "Update + Add Role SA",
        "Deactivate SA",
    ])

    with tab_update:
        csv_upload = st.file_uploader(
            label="Upload CSV/TXT with required columns",
            type=["csv", "txt"],
            accept_multiple_files=False,
            key="cross_update_file_upload",
        )

        if csv_upload is not None:
            csv_data = pd.read_csv(
                csv_upload,
                converters={
                    "HR Code": str,
                    "ID number": str,
                    "Notes": str,
                    "Supervisor code": str,
                    "Role in Bank": str,
                    "Location": str,
                    "DateOfBirth": str,
                    "Gender": str,
                    "First Name": str,
                    "Last Name": str,
                },
            )

            st.subheader("Input Preview")
            st.write(csv_data)

            missing_columns = [column for column in REQUIRED_COLUMNS if column not in csv_data.columns]
            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
            else:
                run_button = st.button(
                    "Run UMC Update DOB/Gender/Name + Homesis Add Role SA",
                    type="primary",
                    key="cross_update_run_btn",
                )

                if run_button:
                    if not ldap_user.strip() or not ldap_pw.strip() or not technical_user.strip() or not technical_pw.strip():
                        st.error("Please provide LDAP credentials for Homesis and Technical credentials for UMC.")
                        return

                    with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
                        umc_page = login_to_umc_site(ldap_user=technical_user, ldap_pw=technical_pw)
                        umc_request = umc_start_session(
                            authenticate_swagger(username=technical_user, password=technical_pw)
                        )
                        homesis_page = login_to_homesis_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

                        if umc_page is None or umc_request is None or homesis_page is None:
                            st.error("Cannot start UMC/Homesis sessions. Please check credentials.")
                            return

                        homesis_page.access_user_managerment()

                        run_result = []
                        for _, row in csv_data.iterrows():
                            hr_code = str(row["HR Code"]).strip()
                            if hr_code == "":
                                run_result.append(
                                    {
                                        "HR Code": hr_code,
                                        "UMC DOB": "SKIPPED",
                                        "UMC Gender": "SKIPPED",
                                        "UMC Name": "SKIPPED",
                                        "Homesis Role SA": "SKIPPED",
                                        "Detail": "Empty HR Code",
                                    }
                                )
                                continue

                            dob_errors = update_dob(
                                umc_page=umc_page,
                                hr_code=hr_code,
                                date_of_birth=str(row["DateOfBirth"]).strip(),
                            )
                            umc_page.get_umc_url()

                            gender_errors = update_gender(
                                umc_page=umc_page,
                                hr_code=hr_code,
                                detail_gender=str(row["Gender"]).strip(),
                            )
                            umc_page.get_umc_url()

                            name_status = update_name(
                                umc_request=umc_request,
                                hr_code=hr_code,
                                first_name=str(row["First Name"]).strip(),
                                last_name=str(row["Last Name"]).strip(),
                            )

                            homesis_errors = add_role_in_bank_SA(
                                homesis_page=homesis_page,
                                hr_code=hr_code,
                                id_number=str(row["ID number"]).strip(),
                                note=str(row["Notes"]).strip(),
                                supervisor_code=str(row["Supervisor code"]).strip(),
                                role=str(row["Role in Bank"]).strip(),
                                location=str(row["Location"]).strip(),
                            )
                            homesis_page.get_homesis_url()
                            homesis_page.access_user_managerment()

                            dob_success = any(ErrorMessage.umc_message.USER_UPDATED in msg for msg in dob_errors)
                            gender_success = any(ErrorMessage.umc_message.USER_UPDATED in msg for msg in gender_errors)
                            homesis_success = any(
                                ErrorMessage.homesis_message.CLICK_SAVE_BUTTON in msg for msg in homesis_errors
                            )
                            detail_messages = dob_errors + gender_errors + homesis_errors
                            if not name_status:
                                detail_messages.append(f"{hr_code} - Failed to update first/last name on UMC")

                            run_result.append(
                                {
                                    "HR Code": hr_code,
                                    "UMC DOB": "OK" if dob_success else "FAIL",
                                    "UMC Gender": "OK" if gender_success else "FAIL",
                                    "UMC Name": "OK" if name_status else "FAIL",
                                    "Homesis Role SA": "OK" if homesis_success else "FAIL",
                                    "Detail": " | ".join(detail_messages),
                                }
                            )

                    result_df = pd.DataFrame(run_result)
                    st.subheader("Execution Result")
                    st.write(result_df)
                    st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)

    with tab_deactivate:
        st.subheader("Deactivate SA in UMC + Remove Role in Bank on Homesis")
        left, right = st.columns(2)

        deactivate_file = left.file_uploader(
            label="Upload SA account list (column: HR Code)",
            type=["csv", "txt"],
            accept_multiple_files=False,
            key="sa_deactivate_file_upload",
        )
        deactivate_text = right.text_area(
            "Or input SA HR code / login (one per line)",
            key="sa_deactivate_text_input",
        )

        reason_for_deactivation = st.selectbox(
            "Select reason for SA deactivation",
            [
                "Mistake 30 days",
                "AF Deactivate",
                "Hard Trigger",
                "Temp Deactivate",
            ],
            key="sa_deactivation_reason",
        )

        deactivation_candidates = []
        if deactivate_file is not None:
            file_data = pd.read_csv(deactivate_file, converters={"HR Code": str})
            st.write(file_data)
            deactivation_candidates = [
                str(row["HR Code"]).strip()
                for _, row in file_data.iterrows()
                if str(row["HR Code"]).strip() != ""
            ]
        elif deactivate_text.strip() != "":
            deactivation_candidates = [
                code.strip()
                for code in deactivate_text.splitlines()
                if code.strip() != ""
            ]

        if deactivation_candidates:
            run_deactivate_btn = st.button(
                "Run Deactivate SA",
                type="primary",
                key="run_deactivate_sa_btn",
            )

            if run_deactivate_btn:
                if not ldap_user.strip() or not ldap_pw.strip() or not technical_user.strip() or not technical_pw.strip():
                    st.error("Please provide LDAP credentials for Homesis and Technical credentials for UMC.")
                    return

                reason_role_map = {
                    "Mistake 30 days": "SALES_AGENT_MISTAKE_30DAYS",
                    "AF Deactivate": "SALES_AGENT_AF_DEACTIVE",
                    "Hard Trigger": "SALES_AGENT_HARD_TRIGGER",
                    "Temp Deactivate": "SALES_AGENT_TEMP_DEACTIVE",
                }
                selected_reason_role = reason_role_map.get(reason_for_deactivation)

                with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
                    umc_request = umc_start_session(
                        authenticate_swagger(username=technical_user, password=technical_pw)
                    )
                    homesis_page = login_to_homesis_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

                    if umc_request is None or homesis_page is None:
                        st.error("Cannot start UMC/Homesis sessions. Please check credentials.")
                        return

                    homesis_page.access_user_managerment()
                    result_rows = []

                    for account_id in deactivation_candidates:
                        is_sa_account = not account_id.upper().startswith(("FPT", "R0", "MW", "MWG"))
                        if not is_sa_account:
                            result_rows.append(
                                {
                                    "Account": account_id,
                                    "UMC Remove Roles": "SKIPPED",
                                    "UMC Add Dismissal": "SKIPPED",
                                    "Homesis Remove Role": "SKIPPED",
                                    "Detail": "Not SA account",
                                }
                            )
                            continue

                        remove_status = remove_multi_role_umc(
                            umc_request=umc_request,
                            login_codes=[account_id],
                            role_list=["HOMESIS", "HOMESIS_USER"],
                        )

                        add_status = False
                        if selected_reason_role is not None:
                            add_status = add_multi_role_umc(
                                umc_request=umc_request,
                                login_codes=[account_id],
                                role_list=[selected_reason_role],
                            )

                        homesis_errors = remove_role_in_bank_SA(
                            homesis_page=homesis_page,
                            hr_code=account_id,
                        )
                        homesis_page.get_homesis_url()
                        homesis_page.access_user_managerment()

                        homesis_status = any(
                            ErrorMessage.homesis_message.CLICK_SAVE_BUTTON in str(msg)
                            for msg in homesis_errors
                        )

                        result_rows.append(
                            {
                                "Account": account_id,
                                "UMC Remove Roles": "OK" if remove_status else "FAIL",
                                "UMC Add Dismissal": "OK" if add_status else "FAIL",
                                "Homesis Remove Role": "OK" if homesis_status else "FAIL",
                                "Detail": " | ".join(homesis_errors),
                            }
                        )

                    st.subheader("SA Deactivation Result")
                    st.write(pd.DataFrame(result_rows))
                    st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)


if __name__ == "__main__":
    main()
