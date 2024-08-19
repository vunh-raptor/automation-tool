import streamlit as st
import pandas as pd

from Activity.homesis_actions import (
    login_to_site,
    add_role_in_bank_RA,
    add_role_in_bank_RA_MW,
    add_role_in_bank_SA,
    add_role_in_bank_RA_FPT,
    add_role_in_bank_RA_New_Segment
)

def main():
    """
    This function is to support SD task interact with Homesis
    """
    #Title of the page
    homesis_page_title = st.title("HOMESIS AUTOMATION HUB")

    # Username & Password Input
    ldap_user = st.text_input("Homesis Username")
    ldap_pw = st.text_input("Password", type="password")

    #Insert excel file for create Homesis account
    csv_upload_homesis_template = st.file_uploader(
        label="Please input Homesis_Role_In_Bank_Template.csv. You can find it here",
        type=["csv", "txt"],
        accept_multiple_files=False,
    )
    
    # Read CSV Data
    if csv_upload_homesis_template is not None:
        csv_data = pd.read_csv(csv_upload_homesis_template, converters={"HR Code": str, "ID number" : str, "Supervisor code" : str,  "Notes" : str, "Role in Bank" : str, "Location" : str})
        result_table = st.write(csv_data)


    #Chose action on Homesis page
    section_divided_caption = st.header("Please chose your action")

    #Chose action on Homesis page
    section_divided_caption = st.subheader("Add role in bank", divider= "red")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["SA Home", "RA Basic", "RA MW", "RA FPT", "RA NS"])
    with tab1:
        st.markdown("Required field:")
        st.text("HR Code, ID number, Notes, Sup Code, Role SA, Location")
        #Add role in bank SA button
        add_role_in_bank_SA_btn = st.button("Add role-in-bank SA")
        #Add role in bank SA for Homesis page
        if add_role_in_bank_SA_btn:
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
                location = row["Location"]
                list_error = add_role_in_bank_SA(homesis_page = homesis_page, hr_code = hr_code, id_number = id_number, note = note, supervisor_code= supervisor, role = role, location = location)
                st.write(list_error)
                homesis_page.get_homesis_url()
                homesis_page.access_user_managerment()


    with tab2:
        st.markdown("Required field:")
        st.text("HR Code, ID number, Notes, Sup Code, Role RA")
        #Add role in bank RA button
        add_role_in_bank_RA_btn = st.button("Add role-in-bank RA")
        #Add role in bank RA for Homesis page
        if add_role_in_bank_RA_btn:
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
                list_error = add_role_in_bank_RA (homesis_page = homesis_page, hr_code = hr_code, id_number = id_number, note = note, supervisor_code= supervisor, role = role)
                st.write(list_error)
                homesis_page.get_homesis_url()
                homesis_page.access_user_managerment()

     
    with tab3:
        st.markdown("Required field:")
        st.text("HR Code, Notes, Role RA")
        #Add role in bank RA MW button
        add_role_in_bank_RA_MW_btn = st.button("Add role-in-bank RA MW")
        #Add role in bank RA MW for Homesis page
        if add_role_in_bank_RA_MW_btn:
            # Start Selenium
            homesis_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
            homesis_page.access_user_managerment()
        
            # Loop through CSV & Search for HR Code and take data from CSV
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                note = row["Notes"]
                role = row["Role in Bank"]
                list_error = add_role_in_bank_RA_MW(homesis_page = homesis_page, hr_code = hr_code, note = note, role = role)
                st.write(list_error)
                homesis_page.get_homesis_url()
                homesis_page.access_user_managerment()


    with tab4:
        st.markdown("Required field:")
        st.text("HR Code, Notes, Role RA, ID number")
        #Add role in bank RA FPT button
        add_role_in_bank_RA_FPT_btn = st.button("Add role-in-bank RA FPT")
        #Add role in bank RA FPT for Homesis page
        if add_role_in_bank_RA_FPT_btn:
            # Start Selenium
            homesis_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
            homesis_page.access_user_managerment()
        
            # Loop through CSV & Search for HR Code and take data from CSV
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                id_number = row["ID number"]
                note = row["Notes"]
                role = row["Role in Bank"]
                list_error = add_role_in_bank_RA_FPT(homesis_page = homesis_page, hr_code = hr_code, id_number = id_number, note = note, role = role)
                st.write(list_error)
                homesis_page.get_homesis_url()
                homesis_page.access_user_managerment()


    with tab5:
        st.markdown("Required field:")
        st.text("HR Code, Notes, Role RA, ID number, Sup Code")
        #Add role in bank RA button
        add_role_in_bank_RA_NS_btn = st.button("Add role-in-bank RA New Segment")
        #Add role in bank RA New Segment for Homesis page
        if add_role_in_bank_RA_NS_btn:
            # Start Selenium
            homesis_page = login_to_site(ldap_user=ldap_user, ldap_pw=ldap_pw)
            homesis_page.access_user_managerment()
        
            # Loop through CSV & Search for HR Code and take data from CSV
            for index, row in csv_data.iterrows():
                hr_code = row["HR Code"]
                id_number = row["ID number"]
                note = row["Notes"]
                role = row["Role in Bank"]
                supervisor = row["Supervisor code"]
                list_error = add_role_in_bank_RA_New_Segment(homesis_page = homesis_page, hr_code = hr_code, id_number = id_number, note = note, role = role, supervisor_code= supervisor)
                st.write(list_error)
                homesis_page.get_homesis_url()
                homesis_page.access_user_managerment()
           
            
 

if __name__ == "__main__":
    main()
