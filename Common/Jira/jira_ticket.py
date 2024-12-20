import json
from Common.constant.jira_constant import JiraConst


class JiraTicket:
    """
    Represents a JIRA ticket.

    Attributes
    - _rawdata (str): The raw data in JSON format.
    - ticket_data (dict): The JSON data of the ticket.

    """

    _rawdata = "{}"
    ticket_data = json.loads(_rawdata)

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
