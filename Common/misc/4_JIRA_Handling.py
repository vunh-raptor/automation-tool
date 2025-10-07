from Activity.jira_action import general_request_reqdata_SINGLE
from Common.Jira.jira_session import JiraSession
import streamlit as st
from Common.supporting import (
    login_status_check,
    logout_render
)

# This is to jump the user back to login if their are not authenticated
login_status_check()
logout_render()


st.write("This page simply for testing Jira Bot, will be designed later")
jql_get_new_ticket_button = st.button(
    'Get new ticket on queue', type='primary')
jql_get_approval_ticket_button = st.button('Get all approval')

# Function to reset the state


def reset_state():
    st.session_state.counter = 0


# Button to reset the counter
if st.button("Reset"):
    reset_state()

# if jql_get_new_ticket_button:
#     """Get all new ticket belong to SD and print it on the screen
#     """
#     session = JiraSession()
#     response = session.search_jql(JiraConst.JqlSearch.GET_NEW_TICKET)
#     st.write("Total ticket is", response._total_tickets)
#     for i in response._issues_list:
#         st.write(response._json_issues)

if jql_get_approval_ticket_button:
    session = JiraSession()
    # response = session.get_linked_ticket_id("ACCVN-4000")
    # st.write("Total tickets are: ", response)
    approval_list = general_request_reqdata_SINGLE(session, "ACCVN-4000")
    st.write("Approval List are:", approval_list)
