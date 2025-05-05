from requests import Response
from string import Template
import json
from Common.Jira.session_request import Session
from Common.constant.jira_constant import JiraConst
from Common.supporting import filter_id_from_response


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
    _BROWSE_TICKET = "issue/{ticket_key}"
    _JQL_SEARCH = "search?jql="
    _TRANSITION = "issue/{ticket_key}/transitions"
    _COMMENT = "issue/{ticket_key}/comment"

    # PARAMs append for JIRA API
    _GENERAL_PARAM = "?fields={param}"
    _ISSUELINKS = "?fields=issuelinks"
    _APPROVAL_SUMMARY_RESOLUTION = "?fields=resolution&fields=summary"

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

    def browse_ticket(self, ticket_key: str, **kwargs):
        """
        Retrieves and parses a specific ticket.

        Parameters:
        - ticket_key (str): The key of the ticket to retrieve.

        Returns:
        - JIRATicket: The parsed JIRA ticket object.
        """
        endpoint = self._BROWSE_TICKET.format(ticket_key=ticket_key)
        if kwargs:
            for value in kwargs.values():
                endpoint = endpoint + \
                    self._GENERAL_PARAM.format(param=value) + "&"
            # By adding ? in the _GENERAL_PARAM, it's required to remove the excess ? in the API request cURL
            endpoint = endpoint.replace("&?", "&")
        else:
            endpoint = self._BROWSE_TICKET.format(ticket_key=ticket_key)

        result = self.get_request(endpoint=endpoint)
        return JiraTicket(result.text)

    # def search_jql(self, jql: str) -> JiraTicketList:
    #     """
    #     Retrieves and parses a specific ticket.

    #     Parameters:
    #     - ticket_key (str): The key of the ticket to retrieve.

    #     Returns:
    #     - JIRATicket: The parsed JIRA ticket object.
    #     """

    #     endpoint = self._JQL_SEARCH + jql

    #     result = self.get_request(endpoint=endpoint)

    #     return JiraTicketList(rawdata=result.text)

    def get_available_transition_id(self, ticket_key: str):
        """
        Retrieves all transitions the specified issue can perform.

        Parameters:
        - ticket_key (str): The key of the ticket to retrieve.

        Returns:
        - JIRATicket: The parsed JIRA ticket object.
        """

        endpoint = self._TRANSITION.format(ticket_key=ticket_key)

        result = self.get_request(endpoint=endpoint)
        return filter_id_from_response(result)

    # def get_linked_ticket_id(self, ticket_key: str) -> list[str]:
    #     """
    #     Retrieves all ID of linked tickets to the specified issue -
    #     Args:
    #         ticket_key (str): key/ID of the ticket

    #     Returns:
    #         list[str]: an ID list of related tickets
    #     """
    #     approval_id_list = []

    #     endpoint = self._BROWSE_TICKET.format(ticket_key=ticket_key) + self._ISSUELINKS

    #     response = self.get_request(endpoint=endpoint)

    #     result = filter_linked_tickets_from_response(response)

    #     for key in result.keys():
    #         approval_id_list.append(str(key))
    #     return approval_id_list

    # def get_affected_account_username(self, ticket_key:str) -> str:
    #     """
    #     Retrieves affected account username in the ticket
    #     Args:
    #         ticket_key (str): key/ID of the ticket

    #     Returns:
    #         str: account username
    #     """
    #     response = self.browse_ticket(ticket_key=ticket_key, params=JiraConst.customfield.AFFECTED_ACCOUNT)
    #     username = response.get_affected_account_username()
    #     return username

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

        # payload = self._TRANSITION_BODY.format(transition_id=transition_id, fields_info=fields_info)
        payload = json.loads(self._TRANSITION_BODY.substitute(
            transition_id=transition_id))

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
            payload = json.loads(
                self._INTERNAL_COMMENT_BODY.substitute(message=message))
        else:
            payload = json.loads(
                self._COMMENT_BODY.substitute(message=message))

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

        # endpoint = self._TRANSITION.format(ticket_key=ticket_key)

        # #payload = self._TRANSITION_BODY.format(transition_id=transition_id, fields_info=fields_info)
        # payload = json.loads(self._TRANSITION_BODY.substitute(transition_id="911"))

        # result = self.post_request(endpoint=endpoint, payload=payload)

        return self.send_transition(ticket_key=ticket_key, transition_id="911")

    def send_progress(self, ticket_key: str) -> Response:
        """This action to send Start Progress action to the ticket

        Args:
            ticket_key (str): the ticket ID

        Returns:
            Response: Response from request call
        """
        return self.send_transition(ticket_key=ticket_key, transition_id="21")

    def send_resolution(self, ticket_key: str, solution: str) -> Response:
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
                                                   f'\"{JiraConst.customfield.SOLUTION}\":' + f'\"{solution}\"' + """
            }
        """)

        print(payload)
        payload = json.loads(payload)
        result = self.post_request(endpoint=endpoint, payload=payload)
        return result

# --------------------------------------------------------------------------------------------------------


class JiraTicket:
    """
    Represents a JIRA ticket.

    Attributes
    - _rawdata (str): The raw data in JSON format.
    - ticket_data (dict): The JSON data of the ticket.

    """

    # _rawdata = "{}"
    # ticket_data = json.loads(_rawdata)

    def __init__(self, rawdata=None, json_data=None) -> None:
        """
        Initializes a JiraTicket object.
        If you want to create a JiraTicket object without any data, use rawdata="{}".

        Args:
            rawdata (str): The raw data to be parsed as JSON.
            json_data (dict): The pre-parsed JSON data.

        Raises:
            ValueError: If both rawdata and json_data are None.

        """
        if rawdata is not None:
            self._rawdata = rawdata
            self.ticket_data = json.loads(self._rawdata)
        else:
            if json_data is not None:
                self.ticket_data = json_data
                self._rawdata = json.dumps(json_data)
            else:
                raise ValueError("Both rawdata and json_data cannot be None.")

    def get_key(self) -> str:
        """
        Returns the key of the JIRA ticket.

        Returns:
            str: The key of the JIRA ticket.
        """
        return self.ticket_data["key"]

    def get_fields(self, field: str) -> str:
        """
        Returns the field value of the JIRA ticket.

        Returns:
            str: The field value of the JIRA ticket.
        """
        return self.ticket_data["fields"][field]

    def get_impact(self) -> str:
        """
        Retrieves the impact of the ticket.
        """
        return self.get_fields(JiraConst.customfield.IMPACT)

    def get_summary(self) -> str:
        """
        Retrieves the title/summary of the ticket
        """
        return self.get_fields(JiraConst.customfield.SUMMARY)

    def get_resolution(self) -> str:
        """
        Retrieves the resolution of the ticket
        """
        try:
            return str(self.ticket_data["fields"][JiraConst.customfield.RESOLUTION]['name'])
        except TypeError:
            pass

    def get_affected_account(self) -> str:
        """
        Retrieves the affected account of the ticket
        """
        return self.get_fields(JiraConst.customfield.AFFECTED_ACCOUNT)

    def get_affected_account_username(self) -> str:
        return str(self.get_affected_account()[0]).split("(")[0]

    def get_edit_account_option(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return self.ticket_data["fields"][JiraConst.customfield.EDIT_ACCOUNT_OPTION]['value']

    # def get_linked_ticket_id(self) -> list[str]:
    #     return_list = []
    #     for fields in self.ticket_data['fields']['issuelinks']:
    #         return_list.append(fields['outwardIssue']['key'])
    #     return return_listo
