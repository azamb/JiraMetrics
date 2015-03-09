from holidays import Holidays
from datetime import datetime, timedelta


canadian_holidays = Holidays(country='CA', prov='ON')

def get_average(times):
    '''Find average work hours in a list of times'''
    times = [time for time in times if time is not None]
    if times:
        return round(sum(times)/len(times), 1)
    return 'N/A'


def get_median(times):
    '''Find median in a list of times'''
    times = [time for time in times if time is not None]
    if times:
        times.sort()
        return times[len(times)/2]
    return 'N/A'


def update_start_date(start_date):
    '''Handle tickets created during the weekend'''
    if start_date.weekday() in (5, 6):
        start_date = start_date.replace(hour=8, minute=59, second=59)
    if start_date.weekday() == 5:
        start_date += timedelta(days=2)
    elif start_date.weekday() == 6:
        start_date += timedelta(days=1)

    return start_date


def calculate_work_hours(start_date, end_date):
    '''
        Calculate work hours between two timestamps.
        Business hours are Monday-Friday from 9:00AM to 5:00PM
    '''
    total_work_hours = 0.0

    start_date = update_start_date(start_date)

    first_day = start_date.date()

    last_day = end_date.date()

    start_time = datetime(
        1900, 1, 1, start_date.hour, start_date.minute, start_date.second
    )
    end_time = datetime(
        1900, 1, 1, end_date.hour, end_date.minute, end_date.second
    )
    work_start = datetime.strptime('08:59:59', '%H:%M:%S')
    work_finish = datetime.strptime('16:59:59', '%H:%M:%S')

    daily_work_hours = (work_finish - work_start).seconds/3600

    if start_time < work_start:
        start_time = work_start

    if start_time > work_finish:
        start_time = work_start
        first_day += timedelta(days=1)

    if end_time > work_finish:
        end_time = work_finish

    current_date = first_day
    last_date = last_day

    while current_date <= last_date:
        is_holiday = current_date in canadian_holidays
        # Don't count weekends and holidays
        if current_date.weekday() not in (5, 6) and not is_holiday:
            # At least a day in between start and end date
            if current_date != first_day and current_date != last_day:
                total_work_hours += daily_work_hours
            # Ticket was not completed the same day
            elif current_date == first_day and current_date != last_day:
                total_work_hours += (work_finish - start_time).seconds/3600.0
            # Reached ticket's date of completion
            elif current_date != first_day and current_date == last_day:
                total_work_hours += (end_time - work_start).seconds/3600.0
            # Ticket was completed same day as started
            elif current_date == first_day and current_date == last_day:
                total_work_hours = (end_time - start_time).seconds/3600.0

        current_date += timedelta(days=1)

    return round(total_work_hours, 1)
