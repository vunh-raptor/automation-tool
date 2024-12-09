import streamlit as st
import pandas as pd

from Common.supporting import (
    bsl_bank_name_crosscheck
)

from Activity.bsl_actions import (
    login_to_site,
    create_bank_branch_single
)

def main():
    """
    This function is to support SD task interact with BSL
    """
    #Title of the page
    st.title("BSL AUTOMATION HUB")

    # Username & Password Input
    ldap_user = st.text_input("LDAP Username")
    ldap_password = st.text_input("Password", type="password")

    # Choose action to take on BSL
    st.subheader("Choose your action on BSL", divider="red")
    
    tab1, tab2, tab3 = st.tabs(["Create bank branches", "Check Ticketing ID", "Other"])
    
    with tab1:
        tab1_exec(ldap_user, ldap_password)
        
    pass

def tab1_exec(username: str, password: str):
    """tab1_exec execute add bank branch function

    Args:
        username (str): str value of login name
        password (str): str value of password
    """
    # Preload Data File to for BSL to compare
    preload_path = r"Common\data\bank_list.txt"
    f = open(preload_path, "r", encoding="utf8")
    bank_name_list = f.readlines()
    
    # Insert excel file for create bank branch
    excel_upload_branch_template = st.file_uploader(
        label="Please upload ticket template file here",
        type=["xlsx"],
        accept_multiple_files=False,
    )
    
    if excel_upload_branch_template is not None:
        read_cols = [1,2,3,4]
        excel_data = pd.read_excel(excel_upload_branch_template, converters={"Bank Name": str, "Bank Branch code": str, "Region and District": str}, usecols=read_cols)
        st.write(excel_data)
        confirm_button = st.button("Confirm & Proceed", type="primary")
        if confirm_button:
            # Process Data
            excel_data[['Region', 'District']] = excel_data['Region and District'].str.split(',', expand=True)
            # Action starts
            bsl_page = login_to_site(username, password)
            bsl_page.click_find_bank()
            for index, row in excel_data.iterrows():
                bank_name = row[excel_data.columns[0]]
                if bsl_bank_name_crosscheck(bank_name_list=bank_name_list, bank_name=bank_name) is True:
                    branch_code = row[excel_data.columns[1]]
                    branch_name = row[excel_data.columns[2]]
                    branch_region = row[excel_data.columns[4]]
                    branch_district = row[excel_data.columns[5]]
                    create_bank_branch_single(bsl_page=bsl_page, bank_name=bank_name, bank_branch_name=branch_name, bank_branch_code=branch_code, region=branch_region, district=branch_district)
                    bsl_page.get_bsl_url()
                    bsl_page.click_find_bank()
                    continue #Continue to next iteration if bank name not valid on correct bank sample
                else:
                    continue


def tab2_exec(username, password):
    # bsl_page = login_to_site(username, password)
    pass
if __name__ == "__main__":
    main()