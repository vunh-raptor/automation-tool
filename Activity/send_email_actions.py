import win32com.client as win32
import pythoncom
import streamlit.components.v1 as components


def send_email_automation (emailSubject, bodyTemplate):
    #intergrate with outlook
    outlook = win32. Dispatch('outlook.application', pythoncom.CoInitialize())
    #create an email
    email = outlook.CreateItem(0)
    #email body
    email.To = "nhu.huynhny@homecredit.vn"
    email.Subject = emailSubject
    email.HTMLBody = bodyTemplate
    
    #This code is for sending by specific email, will be implemented later

    # # If you want to set which address the e-mail is sent from. 
    # # The e-mail needs to be part of your outlook account.
    # From = None
    # for myEmailAddress in outlook.Session.Accounts:
    #     if "_it_sd_group" in str(myEmailAddress):
    #         From = myEmailAddress
    #         break

    # if From != None:
    #     # This line basically calls the "mail.SendUsingAccount = IT_SD@gmail.com" outlook VBA command
    #     email._oleobj_.Invoke(*(64209, 0, 8, 0, From))
    
    email.Send()

