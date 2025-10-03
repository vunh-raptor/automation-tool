import streamlit as st

# This is to jump the user back to login if their are not authenticated
if st.session_state["authenticated"] is not True:
    st.switch_page("main_site.py")

import datetime
import pandas as pd
import streamlit.components.v1 as components
from streamlit_quill import st_quill
from streamlit_ace import st_ace
from Common.constant.css_file import css

from Activity.send_email_actions import send_email_automation
from Common.supporting import (
    login_status_check,
    logout_render
)

# This is to jump the user back to login if their are not authenticated
login_status_check()
logout_render()


def main():
    # This function is to working with sending email task
    # implement css for file upload element
    st.markdown(css.css_send_email_automation_hub, unsafe_allow_html=True)
    # Title of the page
    st.title("Email Automation Hub")

    # Option for chose email template
    option = st.selectbox(
        "Please chose the email template",
        (
            "External Maintenance Notification",
            "Internal Maintenance Notification",
            "Incident Notification",
        ),
        index=None,
    )
    st.divider()
    # Send External Maintenance Notification email
    if option == "External Maintenance Notification":
        # Input fileds of external maintenance email
        left, rigth = st.columns(2, vertical_alignment="bottom")
        start_date = left.date_input(label="Ngày bắt đầu")
        start_time = rigth.time_input(label="Thời gian bắt đầu")
        end_date = left.date_input(label="Ngày kết thúc")
        end_time = rigth.time_input(label="Thời gian kết thúc")
        start_datetime = datetime.datetime.combine(start_date, start_time)
        end_datetime = datetime.datetime.combine(end_date, end_time)
        # Format date and time for English version
        start_datetime_eng = start_datetime.strftime("%B %d, %Y, %X")
        end_datetime_eng = start_datetime.strftime("%B %d, %Y, %X")

        # Array contain value fill in email
        date_start_and_end = {
            "start": start_datetime,
            "end": end_datetime,
            "start_eng": start_datetime_eng,
            "end_eng": end_datetime_eng,
        }

        st.divider()

        # Receiver and cc section

        # To section
        list_to_email = ""
        list_to_email_upload = st.file_uploader(
            "List To emails",
            accept_multiple_files=True,
            type=["csv"],
        )

        # Read CSV Data
        for i in range(len(list_to_email_upload)):
            to_email_data = pd.read_csv(
                list_to_email_upload[i], converters={"Email": str})
            for index, row in to_email_data.iterrows():
                # read each email from csv file
                to_emails = row["Email"]
                # return a list of emails in a type a string
                list_to_email = list_to_email + to_emails + "; "

        to = st.text_area("To", list_to_email)

        st.divider()

        # CC sesion
        list_cc_email = ""
        list_cc_email_upload = st.file_uploader(
            "List CC emails",
            accept_multiple_files=True,
            type=["csv"],
        )

        # Read CSV Data
        for i in range(len(list_cc_email_upload)):
            cc_email_data = pd.read_csv(
                list_cc_email_upload[i], converters={"Email": str})
            for index, row in cc_email_data.iterrows():
                # read each email from csv file
                cc_emails = row["Email"]
                # return a list of emails in a type a string
                list_cc_email = list_cc_email + cc_emails + "; "
        cc = st.text_area("CC", list_cc_email)

        st.divider()

        # BCC section
        list_bcc_email = ""
        list_bcc_email_upload = st.file_uploader(
            "List BCC emails",
            accept_multiple_files=True,
            type=["csv"],
        )

        # Read CSV Data
        for i in range(len(list_bcc_email_upload)):
            bcc_email_data = pd.read_csv(
                list_bcc_email_upload[i], converters={"Email": str})
            for index, row in bcc_email_data.iterrows():
                # read each email from csv file
                bcc_emails = row["Email"]
                # return a list of emails in a type a string
                list_bcc_email = list_bcc_email + bcc_emails + "; "
        bcc = st.text_area("BCC", list_bcc_email)
        st.divider()
        # Define email html template
        HTMLFile = open(
            r"Common\template\external_mail_maintenance_template.html",
            "r",
            encoding="utf8",
        )
        # Load html template
        external_maintenance_notification_html = HTMLFile.read()

        # Fill the input value to the email template and show it in a editor section
        external_mail_maintenance_content = st_ace(
            value=external_maintenance_notification_html.format(
                **date_start_and_end),
            auto_update=True,
        )

        # Show the email content on UI
        st.markdown(external_mail_maintenance_content, unsafe_allow_html=True)

        left, middle, rigth = st.columns(3, vertical_alignment="bottom")

        # Send the full email by click on the button
        send_email_btn = middle.button(
            "Send External Maintenance Notification email", type="primary"
        )
        if send_email_btn:
            send_email_automation(
                receiver=to,
                cc=cc,
                bcc=bcc,
                emailSubject="[MAINTENANCE NOTIFICATION] HCVN THÔNG BÁO BẢO TRÌ HỆ THỐNG ",
                bodyTemplate=external_mail_maintenance_content,
            )

    # Send Internal Maintenance Notification email
    if option == "Internal Maintenance Notification":
        # Input fileds of internal maintenance email
        subject = st.text_input("Subject of the email", max_chars=250)
        description = st.text_input("Email description")
        left, rigth = st.columns(2, vertical_alignment="bottom")
        start_date = left.date_input(label="Ngày bắt đầu")
        start_time = rigth.time_input(label="Thời gian bắt đầu")
        end_date = left.date_input(label="Ngày kết thúc")
        end_time = rigth.time_input(label="Thời gian kết thúc")
        start_datetime = datetime.datetime.combine(start_date, start_time)
        end_datetime = datetime.datetime.combine(end_date, end_time)

        # Format date and time for English version
        start_datetime_eng = start_datetime.strftime("%B %d, %Y, %X")
        end_datetime_eng = end_datetime.strftime("%B %d, %Y, %X")
        impacted_service = st.text_input("Impacted service")

        st.divider()

        # Receiver and cc fields
        # To section
        list_to_email_internal = ""
        list_to_email_upload_internal = st.file_uploader(
            "List To emails of Internal Maitainance",
            accept_multiple_files=True,
            type=["csv"],
        )

        # implement css for file upload element
        st.markdown(css.css_send_email_automation_hub, unsafe_allow_html=True)
        # Read CSV Data
        for i in range(len(list_to_email_upload_internal)):
            to_email_internal_data = pd.read_csv(
                list_to_email_upload_internal[i], converters={"Email": str})
            for index, row in to_email_internal_data.iterrows():
                # read each email from csv file
                to_emails_internal = row["Email"]
                # return a list of emails in a type a string
                list_to_email_internal = list_to_email_internal + to_emails_internal + "; "

        to = st.text_area("To", list_to_email_internal)

        st.divider()

        # CC sesion
        list_cc_email_internal = ""
        list_cc_email_internal_upload = st.file_uploader(
            "List CC emails of Internal Maitainance",
            accept_multiple_files=True,
            type=["csv"],
        )

        # Read CSV Data
        for i in range(len(list_cc_email_internal_upload)):
            cc_email_internal_data = pd.read_csv(
                list_cc_email_internal_upload[i], converters={"Email": str})
            for index, row in cc_email_internal_data.iterrows():
                # read each email from csv file
                cc_emails_internal = row["Email"]
                # return a list of emails in a type a string
                list_cc_email_internal = list_cc_email_internal + cc_emails_internal + "; "
        cc = st.text_area("CC", list_cc_email_internal)

        st.divider()

        # BCC section
        list_bcc_internal_email = ""
        list_bcc_email_internal_upload = st.file_uploader(
            "List BCC emails",
            accept_multiple_files=True,
            type=["csv"],
        )

        # Read CSV Data
        for i in range(len(list_bcc_email_internal_upload)):
            bcc_email_internal_data = pd.read_csv(
                list_bcc_email_internal_upload[i], converters={"Email": str})
            for index, row in bcc_email_internal_data.iterrows():
                # read each email from csv file
                bcc_internal_emails = row["Email"]
                # return a list of emails in a type a string
                list_bcc_internal_email = list_bcc_internal_email + bcc_internal_emails + "; "
        bcc = st.text_area("BCC", list_bcc_internal_email)
        st.divider()

        # Array contain value fill in email
        filled_value = {
            "description": description,
            "start": start_datetime_eng,
            "end": end_datetime_eng,
            "impactedService": impacted_service,
        }

        # Define email html template
        HTMLFile = open(
            r"Common\template\internal_mail_maintenance_template.html",
            "r",
            encoding="utf8",
        )
        # Load html template
        internal_maintenance_notification_html = HTMLFile.read()
        # Fill the input value to the email template and show it in editor section
        internal_mail_maintenance_content = st_ace(
            value=internal_maintenance_notification_html.format(
                **filled_value),
            auto_update=True,
        )

        # Show the email content on UI
        st.markdown(internal_mail_maintenance_content, unsafe_allow_html=True)

        left, middle, rigth = st.columns(3, vertical_alignment="bottom")

        # Send the full email by click on the button
        send_email_btn = middle.button(
            "Send Internal Maintenance Notification email", type="primary"
        )
        if send_email_btn:
            send_email_automation(
                receiver=to,
                cc=cc,
                bcc=bcc,
                emailSubject="[MAINTENANCE NOTIFICATION] " + subject,
                bodyTemplate=internal_mail_maintenance_content,
            )

    # Send Incident Notification email
    if option == "Incident Notification":
        # Input fileds of incident notification email
        incident_ticket_number = st.text_input(
            "Input number of ticket incident", value="INCVN-", max_chars=10
        )
        incident_description = st.text_input("Email Description")
        bussiness_impacted = st.text_input("Business Impacted")
        current_status = st.text_input("Current Status")

        st.divider()

        # Receiver and cc fields
        # To section
        list_to_email_incident = ""
        list_to_email_upload_incident = st.file_uploader(
            "List To emails of Internal Maitainance",
            accept_multiple_files=True,
            type=["csv"],
        )

        # implement css for file upload element
        st.markdown(css.css_send_email_automation_hub, unsafe_allow_html=True)
        # Read CSV Data
        for i in range(len(list_to_email_upload_incident)):
            to_email_incident_data = pd.read_csv(
                list_to_email_upload_incident[i], converters={"Email": str})
            for index, row in to_email_incident_data.iterrows():
                # read each email from csv file
                to_emails_incident = row["Email"]
                # return a list of emails in a type a string
                list_to_email_incident = list_to_email_incident + to_emails_incident + "; "

        to = st.text_area("To", list_to_email_incident)

        st.divider()

        # CC sesion
        list_cc_email_incident = ""
        list_cc_email_incident_upload = st.file_uploader(
            "List CC emails of Internal Maitainance",
            accept_multiple_files=True,
            type=["csv"],
        )

        # Read CSV Data
        for i in range(len(list_cc_email_incident_upload)):
            cc_email_incident_data = pd.read_csv(
                list_cc_email_incident_upload[i], converters={"Email": str})
            for index, row in cc_email_incident_data.iterrows():
                # read each email from csv file
                cc_emails_incident = row["Email"]
                # return a list of emails in a type a string
                list_cc_email_incident = list_cc_email_incident + cc_emails_incident + "; "
        cc = st.text_area("CC", list_cc_email_incident)

        st.divider()
        # BCC section
        list_bcc_incident_email = ""
        list_bcc_email_incident_upload = st.file_uploader(
            "List BCC emails",
            accept_multiple_files=True,
            type=["csv"],
        )

        # Read CSV Data
        for i in range(len(list_bcc_email_incident_upload)):
            bcc_email_incident_data = pd.read_csv(
                list_bcc_email_incident_upload[i], converters={"Email": str})
            for index, row in bcc_email_incident_data.iterrows():
                # read each email from csv file
                bcc_incident_emails = row["Email"]
                # return a list of emails in a type a string
                list_bcc_incident_email = list_bcc_incident_email + bcc_incident_emails + "; "
        bcc = st.text_area("BCC", list_bcc_incident_email)
        st.divider()

        incident_email_filled_value = {
            "ticketNumber": incident_ticket_number,
            "description": incident_description,
            "businessImpact": bussiness_impacted,
            "currentStatus": current_status,
        }
        # Define email html template
        HTMLFile = open(
            r"Common\template\incident_notification_template.html", "r", encoding="utf8"
        )
        # Load html template
        incident_notification_template_html = HTMLFile.read()
        # Fill the input value to the email template and show it in editor section
        incident_notification_content = st_ace(
            value=incident_notification_template_html.format(
                **incident_email_filled_value
            ),
            auto_update=True,
        )
        # Show the email content on UI
        st.markdown(incident_notification_content, unsafe_allow_html=True)

        left, middle, rigth = st.columns(3, vertical_alignment="bottom")

        # Send the full email by click on the button
        send_email_btn = middle.button(
            "Send Incident Notification email",
        )
        if send_email_btn:
            send_email_automation(
                receiver=to,
                cc=cc,
                bcc=bcc,
                emailSubject="[INCIDENT NOTIFICATION]-"
                + "["
                + incident_ticket_number
                + "-"
                + incident_description
                + "]",
                bodyTemplate=incident_notification_content,
            )


if __name__ == "__main__":
    main()
