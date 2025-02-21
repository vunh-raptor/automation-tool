from Common.Jira.jira_session import JiraSession
from Common.Jira.jira_session import JiraTicket
from Common.constant.jira_constant import JiraConst

def general_request_reqdata_SINGLE(jira_session: JiraSession, origin_ticket_key: str) -> list:
    """Get all required information for the bot to run script

    Args:
        jira_session (JiraSession): jira API session to get data
        origin_ticket_key (str): ACCVN ticket, original to child approval tickets

    Returns:
        list: List of approved ticket & Role Name - Example:
    """
    # affected_account = jira_session.get_affected_account_username(ticket_key=origin_ticket_key)
    # approval_id_list = jira_session.get_linked_ticket_id(ticket_key=origin_ticket_key)
    origin_ticket_data = jira_session.browse_ticket(
        ticket_key=origin_ticket_key,
        param1="issuelinks",
        param2=JiraConst.customfield.AFFECTED_ACCOUNT,
        param3=JiraConst.customfield.EDIT_ACCOUNT_OPTION
        )
    affected_account = origin_ticket_data.get_affected_account_username()
    approval_id_list = origin_ticket_data.get_linked_ticket_id()
    role_option = origin_ticket_data.get_edit_account_option()
    return_list = []
    for id in approval_id_list:
        ticket_data = jira_session.browse_ticket(ticket_key=id, param1="resolution", param2="summary")
        # This IF will filter out the ticket that been declined
        if ticket_data.get_resolution() == "Resolved":
            return_list.append(ticket_data.get_summary().replace('Service Request - L2 - "Role Approver - Role" - "', "").replace('"', "") + " - " + "Approved" + " - " + affected_account)
        else:
            return_list.append(ticket_data.get_summary().replace('Service Request - L2 - "Role Approver - Role" - "', "").replace('"', "") + " - " + "Declined" + " - " + affected_account)
    return return_list

