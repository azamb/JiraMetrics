import csv
import sys

from constants import SERVER_URL, USERNAME, PASSWORD
from JiraMetrics import JiraClient

def main():
    # Header row in the csv report
    fieldnames = [
        'Metric', 'Priority', 'Average Work Hours', 'Median Work Hours'
    ]
    ticket_priorities = ['High', 'Medium']

    with open('/var/tmp/jira_metrics.csv', 'wb') as fout:
        dw = csv.DictWriter(fout, fieldnames=fieldnames)
        dw.writerow(dict((fn, fn) for fn in fieldnames))

        jira_client = JiraClient(SERVER_URL, USERNAME, PASSWORD)

        print("Report is generating")

        for priority in ticket_priorities:
            issues = jira_client.fixed_bugs_by_priority(priority)

            # Team aggregates by priority
            dw.writerow(
                jira_client.opened_to_resolved(issues, priority)
            )
            dw.writerow(
                jira_client.in_progress_to_resolved(issues, priority)
            )
            dw.writerow(
                jira_client.open_to_assigned(issues, priority)
            )

if __name__ == '__main__':
    sys.exit(main())
