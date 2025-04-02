import streamlit as st
from Common.db_connection import DBConnection

def main():

    db_path = "\\\\vn-vwl5050\\group2\\SD_Storage\\AutomationHubDB\\automation_hub.db"
    db_connection = DBConnection(db_path)


    st.write("This page is using for test the database accesss")
    query = st.text_input("sql query")
    execute_button = st.button("Execute",type="primary")
    if execute_button:
        db_connection.execute_query(query=query)
    st.write(db_connection.fetch_data_from_db(query))



if __name__ == "__main__":
    main()
