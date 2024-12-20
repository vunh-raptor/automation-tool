import json
from Common.Jira.jira_ticket import JiraTicket


class JiraTicketList:
    """
    Represents a list of JIRA tickets.

    Attributes:
    - _rawdata (str): The raw data in JSON format.
    - _json_master_data (dict): The JSON master data.
    - _total_tickets (int): The total number of tickets.
    - _json_issues (list): The list of JSON issues.
    - _issues_list (list[JiraTicket]): The list of JiraTicket objects.
    """

    _rawdata = "{}"
    _json_master_data = json.loads(_rawdata)
    _total_tickets = 0
    _json_issues = json.loads(_rawdata)
    _issues_list = []

    def __init__(self, rawdata="{}", json_master_data=None, json_issues=None) -> None:
        """
        Initializes a JiraTicketList object.

        Parameters:
        - rawdata (str): The raw data in JSON format.
        - json_master_data (dict): The JSON master data.
        - json_issues (list[JiraTicket]): The list of JiraTicket objects.

        Returns:
        None
        """

        # Logic to generate a list of JiraTicket, priority of the data source is rawdata > json_master_data > json_issues

        if rawdata != self._rawdata:

            # Generate all the data base on rawdata
            self._rawdata = rawdata
            self._json_master_data = json.loads(rawdata)
            self._total_tickets = self._json_master_data["total"]
            self._json_issues = self._json_master_data["issues"]

            # Generate a list of issues based on the _json_issues
            self.parsing_issues_from_json_issues()

        else:
            if json_master_data is not None:
                # Generate all the data base on _json_master_data
                self._json_master_data = json_master_data

                # Dumping back the raw data to self._rawdata
                self._rawdata = json.dumps(json_master_data)

                # Generate a list of issues based on the _json_issues
                self.parsing_issues_from_json_issues()

            else:
                if json_issues is not None:
                    # Generate all the data base on _json_issues
                    self._json_issues = json_issues
                    self._total_tickets = len(json_issues)
                else:
                    raise ValueError("All the data sources cannot be Empty.")

    def parsing_issues_from_json_issues(self) -> None:
        """
        Parsing all the issues in the list.
        """

        for issue in self._json_issues:
            list.append(self._issues_list, JiraTicket(json_data=issue))
