from jira.client import JIRA
from helpers import get_average, get_median
import metrics

class JiraClient(object):

    def __init__(self, server_url, username, password):
        self.jira_client = JIRA(
            options={
                'server': server_url,
                'verify': False
            },
            basic_auth=(username, password)
        )

    def fixed_bugs_by_priority(self, priority):
        '''
            Find all the bugs the team has fixed
        '''
        query = (
            'assignee in membersOf("{TEAM_NAME}") AND '
            'issuetype = Bug AND priority = {0} AND status in '
            '(Closed, Resolved) AND resolution = Fixed'
        ).format(priority)

        tickets = self.jira_client.search_issues(
            query,
            expand='changelog',
            maxResults=None
        )

        return tickets

    def opened_to_resolved(self, issues, priority):
        opened_to_resolved = [
            metrics.opened_to_resolved(issue) for issue in issues
        ]
        return self.build_row(
            'Hours until Resolved',
            priority,
            opened_to_resolved
        )

    def in_progress_to_resolved(self, issues, priority):
        in_progress_to_resolved = [
            metrics.in_progress_to_resolved(issue) for issue in issues
        ]
        return self.build_row(
            'Hours in progress',
            priority,
            in_progress_to_resolved
        )

    def open_to_assigned(self, issues, priority):
        open_to_assigned = [
            metrics.open_to_assigned(issue) for issue in issues
        ]
        return self.build_row(
            'Response Time',
            priority,
            open_to_assigned
        )

    def build_row(self, metric, priority, tickets):
        row = {
            'Metric': metric,
            'Priority': priority,
            'Average Work Hours': get_average(tickets),
            'Median Work Hours': get_median(tickets),
        }
        return row
