# What is it:

* This is a tool that creates a csv report with team performance metrics.
  * For example: How long on average it takes our team to solve hight priority tickets.
* It uses the JQL and a Jira client for Python.

# Why:

* 360pi Developers are split into Product Development and Customer Services.
  * We deal with anything customer related that needs technical intervention.
* It became obvious very quickly that we needed to answer to our customers in time units and not story points.
* We wanted to be able to tell a customer with some certainty how long a particular issue would take to be resolved.
* So we decided to use past performance as an indicator to help us answer that question.
* Our team uses kanban for resolving issues that our project managers raise.

## Possible routes:

* Native time tracking from jira is intrusive. We didn’t want to change our workflow just for this.
* We found another plugin in Jira marketplace that tracked time based on the status of the ticket (less intrusive).
  * cons:
* Jira has two version. Server and cloud. We use Jira on demand(cloud version) and to this date this plugin is only available for the server version.

## Metric Definitions:
### Response time:

* Work hours from ticket creation until it is first assigned to a member of the technical services team.

### Hours in progress:

* Number of work hours a ticket spends between the in progress state and resolved state.

### Hours until resolved:

* Work hours between ticket creation and resolution.

## Assumptions and limitations:

1. The only tickets considered are fixed bugs created since Q2.
2. Work hours are between 9am-5pm from Monday to Friday.
3. Last assignee for a ticket gets all work hours attributed to a ticket. Even if there were multiple assignees.
4. Blocked issues are not handled.
5. Does not handle properly tickets that were not created as bugs and later converted to bugs. e.g: DEV-18234

Code explanation:

* main.py:
  * Opens and writes a new csv file.
  * Connects to our jira account.
  * Queries tickets.
* JiraMetrics.py:
  * Creates a JiraClient.
  * Methods that call each particular metric.
  * Builds the csv rows.
* metrics.py
  * Contains logic behind each of the performance metrics we defined.
  * Calls the helpers that calculate average/median work hours.
* helpers.py
  * small helper functions to calculate average and median.
  * Main helper function that calculates work hours between two timestamps.