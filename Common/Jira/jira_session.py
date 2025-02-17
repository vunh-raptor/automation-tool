from requests import Response
from string import Template
import json
from Common.Jira.jira_ticket import JiraTicket
from Common.Jira.jira_ticket_list import JiraTicketList
from Common.Jira.session_request import Session
from Common.Jira.session_request import get_id_from_response
from Common.constant import jira_constant


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
    _COMMENT = "issue/{ticket_key}/comment"

    # BODY TEMPLATE FOR JIRA API
    _TRANSITION_BODY = Template("""
    { 
        "transition":{
         "id":"${transition_id}"
        }
        ${optional_message}
    }
    """)
    
    _COMMENT_BODY = Template(
        """{
            "body":"${message}"
        }
        ${optional_message}
        """
    )
    
    _INTERNAL_COMMENT_BODY = Template(
        """{
        "body": "${message}",
        "properties": [
            {
            "key": "sd.public.comment",
            "value":{
                "internal": true
            }
            }
        ]
        }
        """
    )
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
    
    def send_transition(self, ticket_key: str, transition_id: str) -> Response:
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

        #payload = self._TRANSITION_BODY.format(transition_id=transition_id, fields_info=fields_info)
        payload = json.loads(self._TRANSITION_BODY.substitute(transition_id=transition_id))

        result = self.post_request(endpoint=endpoint, payload=payload)
        return result

    def add_comment(self, ticket_key: str, message: str, internal: bool = False) -> Response:
        """
        Input a comment to the designated ticket
        
        Params:
            ticket_key (str): the key of the ticket that need to input comment
            message (str): Message that needed to be input
            internal (bool): Value define if whether the comment is Internal or not. True mean Internal
        
        Returns:
            result: The result of add comment request
        """
        endpoint = self._COMMENT.format(ticket_key=ticket_key)
        payload = ""
        if internal:
             # Using json loads parse the text string into a valid JSON object that Jira Server can understand, avoid having response 400 
            payload = json.loads(self._INTERNAL_COMMENT_BODY.substitute(message=message))
        else:
            payload = json.loads(self._COMMENT_BODY.substitute(message=message))
        
        result = self.post_request(endpoint=endpoint, payload=payload)
        return result
        
    def extract_comment(self, ticket_key: str):
        """
        Extract all comment of the designated ticket

        Args:
            ticket_key (str): _description_
        """
        
    def send_classify(self, ticket_key: str) -> Response:
        """This action to send classification action to the ticket

        Args:
            ticket_key (str): the ticket ID

        Returns:
            Response: response from request call
        """
        
        endpoint = self._TRANSITION.format(ticket_key=ticket_key)

        #payload = self._TRANSITION_BODY.format(transition_id=transition_id, fields_info=fields_info)
        payload = json.loads(self._TRANSITION_BODY.substitute(transition_id="911"))

        result = self.post_request(endpoint=endpoint, payload=payload)
        return result
    
    def send_progress(self, ticket_key:str) -> Response:
        """This action to send Start Progress action to the ticket

        Args:
            ticket_key (str): the ticket ID

        Returns:
            Response: Response from request call
        """
        
        endpoint = self._TRANSITION.format(ticket_key=ticket_key)
        
        payload = json.loads(self._TRANSITION_BODY.substitute(transition_id="21"))

        result = self.post_request(endpoint=endpoint, payload=payload)
        return result
    
    def send_resolution(self, ticket_key:str, solution:str) -> Response:
        """This action to send Resolve action to the ticket

        Args:
            ticket_key (str): the ticket ID
            solution (str): Brief describe of the ticket solution

        Returns:
            Response: Response from request call
        """       
         
        endpoint = self._TRANSITION.format(ticket_key=ticket_key)

        # Solution payload in the Rest request, append to the _TRANSITION_BODY
        payload = self._TRANSITION_BODY.substitute(transition_id="721", optional_message=""",
        "fields":
            {""" +
            f'\"{jira_constant.JiraConst.customfield.SOLUTION}\":' + f'\"{solution}\"' + """
            }
        """)
        
        print(payload)
        payload = json.loads(payload)
        result = self.post_request(endpoint=endpoint, payload=payload)
        return result