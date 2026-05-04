import pandas as pd
import streamlit as st

import Common.constant.app_message as app_msg
from Common.constant import app_logic_exception
from Common.constant.error_message import ErrorMessage
from Common.supporting import login_status_check, logout_render

from Activity.umc_actions import (
    login_to_site as login_to_umc_site,
    update_dob,
    update_gender,
)
from Activity.homesis_actions import (
    login_to_site as login_to_homesis_site,
    add_role_in_bank_SA,
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

    csv_upload = st.file_uploader(
        label="Upload CSV/TXT with required columns",
        type=["csv", "txt"],
        accept_multiple_files=False,
    )

    if csv_upload is None:
        return

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
        return

    run_button = st.button(
        "Run UMC Update DOB/Gender + Homesis Add Role SA",
        type="primary",
    )

    if not run_button:
        return

    if not ldap_user.strip() or not ldap_pw.strip() or not technical_user.strip() or not technical_pw.strip():
        st.error("Please provide LDAP credentials for Homesis and Technical credentials for UMC.")
        return

    with st.spinner(app_msg.APP_MESSAGE.APP_RUNNING_MSG):
        umc_page = login_to_umc_site(ldap_user=technical_user, ldap_pw=technical_pw)
        homesis_page = login_to_homesis_site(ldap_user=ldap_user, ldap_pw=ldap_pw)

        if umc_page is None or homesis_page is None:
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

            run_result.append(
                {
                    "HR Code": hr_code,
                    "UMC DOB": "OK" if dob_success else "FAIL",
                    "UMC Gender": "OK" if gender_success else "FAIL",
                    "Homesis Role SA": "OK" if homesis_success else "FAIL",
                    "Detail": " | ".join(dob_errors + gender_errors + homesis_errors),
                }
            )

    result_df = pd.DataFrame(run_result)
    st.subheader("Execution Result")
    st.write(result_df)
    st.write(app_msg.APP_MESSAGE.APP_FINISH_MSG)


if __name__ == "__main__":
    main()
