import streamlit as st
from Common.Jira.jira_session import JiraSession

one_ticket_button = st.button('Debugging button')

"""
This script handles JIRA ticket handling using the Streamlit framework.

The script imports the necessary modules and defines a debugging button using Streamlit.
When the debugging button is clicked, it creates a JIRA session and browses a specific ticket.
The ticket key is then retrieved using the `get_key()` method.

Note: Make sure to replace 'INCVN-23838' with the actual ticket key you want to browse.
"""

jql_search_bar = st.text_input('Enter SQL search query')
jql_search_button = st.button('Search')

transition_search_bar = st.text_input('Enter ticket for transition lookup')
transition_search_button = st.button('Transition lookup')

if one_ticket_button:
    session = JiraSession()
    
    ticket = session.browse_ticket('INCVN-23838')
    ticket.get_key()
    ticket.get_impact()

if jql_search_button:
    session = JiraSession()
    session.search_jql(jql_search_bar)
    
if transition_search_button:
    session = JiraSession()
    session.get_available_transition_id(transition_search_bar)