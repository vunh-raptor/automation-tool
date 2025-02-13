import streamlit as st
from Common.Jira.jira_session import JiraSession
from Common.constant.jira_constant import JiraConst


st.write("This page simply for testing Jira Bot, will be designed later")
jql_get_new_ticket_button = st.button('Get new ticket on queue', type='primary')

# Function to reset the state
def reset_state():
    st.session_state.counter = 0

# Button to reset the counter
if st.button("Reset"):
    reset_state()

if jql_get_new_ticket_button:
    """Get all new ticket belong to SD and print it on the screen
    """
    session = JiraSession()
    response = session.search_jql(JiraConst.JqlSearch.GET_NEW_TICKET)
    st.write("Total ticket is", response._total_tickets)
    for i in response._issues_list:
        st.write(response._json_issues)


