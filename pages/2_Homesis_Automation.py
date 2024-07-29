import streamlit as st
import pandas as pd

from Activity.homesis_actions import (
    login_to_site,
    create_sa_account
)

def main():
    """
    This function is to support SD task interact with Homesis
    """


    # Username & Password Input
    ldap_user = st.text_input("Homesis Username")
    ldap_pw = st.text_input("Password", type="password")

    #Insert excel file for create Homesis account
    csv_upload_homesis_template = st.file_uploader(
        label="Please insert template for create SA",
        type=["csv", "txt"],
        accept_multiple_files=False,
    )
    
    # Read CSV Data
    if csv_upload_homesis_template is not None:
        csv_data = pd.read_csv(csv_upload_homesis_template, converters={"HR Code": str, "ID number" : str, "Supervisor code" : str})
        result_table = st.write(csv_data)
 
    #Chose action on Homesis page
    section_divided_caption = st.header("Please chose your action")

    #Creat SA button
    create_account_for_sa_button = st.button("Create Account")

    
    #Create SA on homesis page
    if create_account_for_sa_button:
        # Start Selenium
        homesis_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
        homesis_page.access_user_managerment()
      
        # Loop through CSV & Search for HR Code and take data from CSV
        for index, row in csv_data.iterrows():
            hr_code = row["HR Code"]
            id_number = row["ID number"]
            note = row["Notes"]
            supervisor = row["Supervisor code"]
            role = row["Role in Bank"]
            create_sa_account (homesis_page = homesis_page, hr_code = hr_code, id_number = id_number, note = note, supervisor_code= supervisor, role = role)
            homesis_page.get_homesis_url()
            homesis_page.access_user_managerment()

if __name__ == "__main__":
    main()
