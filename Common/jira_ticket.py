from Common.constant.jira_constant import JiraConst
from Common import supporting

import logging


class jira_ticket:
    def __init__(self, ticket: any) -> None:
        """_summary_

        Args:
            flag (bool): _description_
            value (any): _description_
        """

        self.jira_session = supporting.jira_Auth()
        self.insight_session = supporting.jira_insight_Auth()
        self.ticket_id = ticket
        try:
            # Initiate Issue Object for this ticket
            self.value = self.jira_session.issue(ticket)
            self.flag = True
        except Exception as e:
            self.flag = False
            logging.warning(e)
            logging.warning("There is no ticket action!")

    def get_customfield_value(self, field: str) -> any:
        try:
            result = getattr(self.value.fields, field)
            return result
        except Exception as e:
            logging.critical(e)
            logging.critical("Cannot find the named customfield")
            return None

    def ticket_comment(self, comment: str) -> bool:
        """Function to comment on ticket

        Args:
            ticket (str): String ticket number
            comment (str): String intended comment
        """
        if self.flag:
            self.jira_session.add_comment(self.ticket_id, comment)
            return True
        return False

    def ticket_assign_HCG(self, HCG: str) -> None:
        """Function to assign assignee for the ticket

        Args:
            ticket (str): String number of the ticket
            HCG (str): Intended assignee of the ticket
        """
        if self.flag:
            self.jira_session.assign_issue(self.ticket_id, HCG)
            self.ticket_comment(
                comment="self.jira Auto bot cannot process this ticket, assigning to Service Desk Technician"
            )
        else:
            logging.error("Cannot assign ticket!")

    def ticket_transition(self, transition) -> bool:
        """This is used to define ticket transition mini functions

        Args:
            ticket (str): String for ticket number
            resolve_reply (str, optional): Solution post on ticket when resolved ticket. Defaults to "Resolved (Bot Default Action)".
            reject_reply (str, optional): Reject comment to user when reject ticket. Defaults to "Rejected (Bot Default Action)".

        Returns:
            bool: _description_
        """
        if self.flag:
            # Check if there's any comment"
            self.jira_session.transition_issue(self.ticket_id, transition)
            return True
        return False

    def ticket_reject(self, reject_reason: str) -> bool:
        if self.flag:
            # Check if there's any comment"
            self.jira_session.transition_issue(
                self.ticket_id,
                JiraConst.TransitionID.REJECT,
                fields={JiraConst.customfield.REJECT_REASON_DESCRIPTION: reject_reason},
            )
            return True
        return False

    def ticket_resolve(self, resolve_reason: str) -> bool:
        if self.flag:
            # Check if there's any comment"
            self.jira_session.transition_issue(
                self.ticket_id,
                JiraConst.TransitionID.RESOLVE,
                fields={JiraConst.customfield.RESOLUTION: resolve_reason},
            )
            return True
        return False

    def get_attachment_in_ticket(self, write_path: str = "Data.xlsx") -> bool:
        if attachment_list := self.value.fields.attachment:
            for attachment in attachment_list:
                file = self.jira_session.attachment(attachment.id)
                with open(write_path, "wb") as f:
                    f.write(file.get())
                    return True
        else:
            return False
