from constants import DATE_FORMAT
from datetime import datetime
from helpers import calculate_work_hours


def get_timestamps(issue, field, toString):
    '''
        Loop through ticket history and return list
        of timestamps that meet field and toString
        condition
    '''
    timestamps = []
    for history in issue.changelog.histories:
        for item in history.items:
            if field in item.field and item.toString == toString:
                timestamp = datetime.strptime(
                    history.created.split('.')[0],
                    DATE_FORMAT
                )
                timestamps.append(timestamp)

    return timestamps


def get_opened_date(issue):
    '''
        Get timestamp of the date the ticket was opened.
        Use the date of the last priority change if it exists
        instead.
    '''
    priority = issue.fields.priority.name
    timestamps = get_timestamps(issue, 'priority', priority)

    if timestamps:
        return timestamps[-1]
    else:
        return datetime.strptime(
            issue.fields.created.split('.')[0],
            DATE_FORMAT
        )


def timestamp_of_first_assignee(issue):
    '''Return first timestamp of assignee change'''
    queue_name = 'Technical Services Queue'

    for history in issue.changelog.histories:
        for item in history.items:
            if 'assignee' in item.field and item.toString != queue_name:
                return datetime.strptime(
                    history.created.split('.')[0],
                    DATE_FORMAT
                )


def opened_to_resolved(issue):
    '''
        Calculate work hours between ticket creation
        and resolution.
    '''
    opened_date = get_opened_date(issue)
    resolved_dates = get_timestamps(issue, 'status', 'Resolved')
    reopened_dates = get_timestamps(issue, 'status', 'Reopened')

    if resolved_dates:
        if reopened_dates:
            return calculate_work_hours(opened_date, resolved_dates[0])
        else:
            # Ticket was reopened
            total_work_hours = calculate_work_hours(
                opened_date, resolved_dates.pop(0)
            )

            for reopened, resolved in zip(reopened_dates, resolved_dates):
                total_work_hours += calculate_work_hours(reopened, resolved)

            return total_work_hours

    else:
        # Ticket went straight to closed
        resolved_date = get_timestamps(issue, 'status', 'Closed')[-1]
        return calculate_work_hours(opened_date, resolved_date)


def in_progress_to_resolved(issue):
    '''
        Calculate work hours a ticket spends between
        in progress and resolved.
    '''
    in_progress_dates = get_timestamps(issue, 'status', 'In Progress')
    resolved_dates = get_timestamps(issue, 'status', 'Resolved')
    reopened_dates = get_timestamps(issue, 'status', 'Reopened')

    if in_progress_dates:
        if reopened_dates:
            resolved = datetime.strptime(
                issue.fields.resolutiondate.split('.')[0],
                DATE_FORMAT
            )

            return calculate_work_hours(in_progress_dates[0], resolved)
        else:
            # Ticket was reopened
            total_work_hours = 0.0
            for inprogress, resolved in zip(in_progress_dates, resolved_dates):
                total_work_hours += calculate_work_hours(inprogress, resolved)

            return total_work_hours


def open_to_assigned(issue):
    '''
        Calculate work hours between ticket
        creation and the first time it's assigned.
    '''
    opened_date = get_opened_date(issue)

    assigned_date = timestamp_of_first_assignee(issue)

    if opened_date and assigned_date:
        return calculate_work_hours(opened_date, assigned_date)
