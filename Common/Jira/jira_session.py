from requests import Response
from Common.Jira.jira_ticket import JiraTicket
from Common.Jira.jira_ticket_list import JiraTicketList
from Common.Jira.session_request import Session
from Common.Jira.session_request import get_id_from_response


class JiraSession(Session):
    """
    A class representing a JIRA session.

    Attributes:
    - DEFAULT_TOKEN (str): The default authentication token.
    - authen_token (BearerAuth): The authentication token.
    - url (str): The URL of the JIRA server.

    Methods:
    - __init__(self, token:str=DEFAULT_TOKEN, url:str='https://sd.homecredit.net/rest/api/2/'): Initializes a JIRA session object.
    - parse_ticket(self, result): Parses the result of a ticket request.
    - browse_ticket(self, ticket_key:str): Retrieves and parses a specific ticket.
    """

    # DEFAULT cURL for JIRA API
    _DEFAULT_URL = "https://sd.homecredit.net/rest/api/2/"
    _BROWSE_TICKET = "issue/"
    _JQL_SEARCH = "search?jql="
    _TRANSITION = "issue/{ticket_key}/transitions"

    # BODY TEMPLATE FOR JIRA API
    _TRANSITION_BODY = """
    { 

        "transition":{
         "id":"{transition_id}"
        },
        "fields":{
            {fields_info}
        }
    }
    """

    # This might range from browsing ticket, searching ticket to commit various workflow.

    def browse_ticket(self, ticket_key: str) -> JiraTicket:
        """
        Retrieves and parses a specific ticket.

        Parameters:
        - ticket_key (str): The key of the ticket to retrieve.

        Returns:
        - JIRATicket: The parsed JIRA ticket object.
        """

        endpoint = self._BROWSE_TICKET + ticket_key

        result = self.get_request(endpoint=endpoint)
        return JiraTicket(result.text)

    def search_jql(self, jql: str) -> JiraTicketList:
        """
        Retrieves and parses a specific ticket.

        Parameters:
        - ticket_key (str): The key of the ticket to retrieve.

        Returns:
        - JIRATicket: The parsed JIRA ticket object.
        """

        endpoint = self._JQL_SEARCH + jql

        result = self.get_request(endpoint=endpoint)

        return JiraTicketList(rawdata=result.text)


    def get_available_transition_id(self, ticket_key: str):
        """
        Retrieves and parses a specific ticket.

        Parameters:
        - ticket_key (str): The key of the ticket to retrieve.

        Returns:
        - JIRATicket: The parsed JIRA ticket object.
        """

        endpoint = self._TRANSITION.format(ticket_key=ticket_key)

        result = self.get_request(endpoint=endpoint)
        return get_id_from_response(result)
    
    def send_transition(self, ticket_key: str, transition_id: str, fields_info: str = ""):
        """
        Sends a transition request to the JIRA server.

        Parameters:
        - ticket_key (str): The key of the ticket to transition.
        - transition_id (str): The ID of the transition to perform.
        - fields_info (dict): The fields to include in the transition request.

        Returns:
        - result: The result of the transition request.
        """

        endpoint = self._TRANSITION.format(ticket_key=ticket_key)

        payload = self._TRANSITION_BODY.format(transition_id=transition_id, fields_info=fields_info)

        result = self.post_request(endpoint=endpoint, payload=payload)
        return result
