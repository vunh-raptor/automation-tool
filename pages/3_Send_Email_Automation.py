import datetime
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_quill import st_quill
from streamlit_ace import st_ace
from Common.template.email_automation_hub_template import (
    external_maintenance_notification_html,
    internal_maintenance_notification_html,
    incident_notification_template_html
    

)
from Activity.send_email_actions import(
    send_email_automation
)



def main():
#This function is to working with sending email task

   #Title of the page
   st.title("Email Automation Hub")

   #Option for chose email template
   option = st.selectbox(
        "Please chose the email template",
        (   "External Maintenance Notification",
            "Internal Maintenance Notification", 
            "Incident Notification",
            ),
        index=None,
        )
   st.divider()
   #Send External Maintenance Notification email
   if option == "External Maintenance Notification":
        left, rigth = st.columns(2, vertical_alignment="bottom")     
        start_date = left.date_input(label="Ngày bắt đầu")
        start_time = rigth.time_input(label= "Thời gian bắt đầu")
        end_date = left.date_input(label="Ngày kết thúc")
        end_time = rigth.time_input(label= "Thời gian kết thúc")
        start_datetime = datetime.datetime.combine(start_date, start_time)
        end_datetime = datetime.datetime.combine(end_date, end_time)
        start_datetime_eng = start_datetime.strftime("%B %d, %Y, %X")
        end_datetime_eng = start_datetime.strftime("%B %d, %Y, %X")
        date_start_and_end = { 'start': start_datetime, 'end': end_datetime, 'start_eng':start_datetime_eng, 'end_eng':end_datetime_eng }
          
        external_mail_maintenance_content = st_ace(value = external_maintenance_notification_html.format(**date_start_and_end), auto_update= True)
        st.markdown(external_mail_maintenance_content, unsafe_allow_html=True)
        left,middle, rigth = st.columns(3, vertical_alignment="bottom")
        send_email_btn = middle.button("Send External Maintenance Notification email", type= "primary")
        if send_email_btn:
            send_email_automation("External Maintenance Notification",external_mail_maintenance_content)
   
    #Send Internal Maintenance Notification email
   if option == "Internal Maintenance Notification":
        subject = st.text_input("Subject of the email",max_chars=250)
        description = st.text_input("Email description")
        left, rigth = st.columns(2, vertical_alignment="bottom")
        start_date = left.date_input(label="Ngày bắt đầu")
        start_time = rigth.time_input(label= "Thời gian bắt đầu")
        end_date = left.date_input(label="Ngày kết thúc")
        end_time = rigth.time_input(label= "Thời gian kết thúc")
        start_datetime = datetime.datetime.combine(start_date, start_time)
        end_datetime = datetime.datetime.combine(end_date, end_time)
        start_datetime_eng = start_datetime.strftime("%B %d, %Y, %X")
        end_datetime_eng = end_datetime.strftime("%B %d, %Y, %X")
        impacted_service = st.text_input("Impacted service")
        filled_value = { 'description': description, 'start':start_datetime_eng, 'end':end_datetime_eng, 'impactedService':impacted_service }
        internal_mail_maintenance_content = st_ace(value = internal_maintenance_notification_html.format(**filled_value), auto_update= True)
        st.markdown(internal_mail_maintenance_content, unsafe_allow_html=True)
        left,middle, rigth = st.columns(3, vertical_alignment="bottom")
        send_email_btn = middle.button("Send Internal Maintenance Notification email", type= "primary")
        if send_email_btn:
            send_email_automation("[MAINTENANCE NOTIFICATION] " + subject, internal_mail_maintenance_content)

    #Send Incident Notification email
   if option == "Incident Notification":
       incident_ticket_number = st.text_input("Input number of ticket incident",value= "INCVN-", max_chars=10)
       incident_description = st.text_input("Email Description")
       bussiness_impacted = st.text_input("Business Impacted")
       current_status = st.text_input("Current Status")
       incident_email_filled_value = { 'ticketNumber': incident_ticket_number, 'description':incident_description, 'businessImpact':bussiness_impacted, 'currentStatus':current_status }
       incident_notification_content = st_ace(value = incident_notification_template_html.format(**incident_email_filled_value), auto_update= True)
       st.markdown(incident_notification_content, unsafe_allow_html=True)
       left,middle, rigth = st.columns(3, vertical_alignment="bottom")
       send_email_btn = middle.button("Send Incident Notification email", type= "primary")
       if send_email_btn:
        send_email_automation("[INCIDENT NOTIFICATION]-" + "[" + incident_ticket_number + "-" + incident_description + "]" , incident_notification_content)       

       

if __name__ == "__main__":
    main()
