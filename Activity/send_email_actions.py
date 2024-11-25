import win32com.client as win32
import pythoncom
import streamlit.components.v1 as components
import os


def send_email_automation(
    receiver: str, cc: str, bcc: str, emailSubject: str, bodyTemplate: str
):
    """This funtion is will execute step by step sending an email using python

    Args:
        receiver (str): receivers of the email
        cc (str): cc of the email
        emailSubject (str): subject of the email
        bodyTemplate (str): email content
    """
    # intergrate with outlook
    outlook = win32.Dispatch("outlook.application", pythoncom.CoInitialize())
    # create an email
    email = outlook.CreateItem(0)
    # email body
    email.To = receiver
    email.CC = cc
    email.BCC = bcc
    email.Subject = emailSubject
    email.HTMLBody = bodyTemplate
    # Get the path of the file on local device
    current_directory = os.path.dirname(__file__)
    relative_path = os.path.join(
        current_directory, "..", "Common", "template", "maintenace_images.jpg"
    )
    # This code is for sending by specific email
    # The e-mail needs to be part of your outlook account.
    attachment = email.Attachments.Add(relative_path)
    attachment.PropertyAccessor.SetProperty(
        "http://schemas.microsoft.com/mapi/proptag/0x3712001F", "image_id"
    )
    From = None
    for myEmailAddress in outlook.Session.Accounts:
        if "_IT_SD@homecredit.vn" in str(myEmailAddress):
            From = myEmailAddress
            break

    if From != None:
        # This line basically calls the "mail.SendUsingAccount = specific account" outlook VBA command
        email._oleobj_.Invoke(*(64209, 0, 8, 0, From))

    email.Display(False)
    email.Send()
