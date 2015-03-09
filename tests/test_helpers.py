import unittest
from datetime import datetime

from JiraMetrics.helpers import calculate_work_hours


class TestCalculateWorkHours(unittest.TestCase):

    def test_weekend_ticket(self):
        '''
        Ticket created and completed over the weekend.
        '''
        saturday = '2014-07-19T08:59:59'
        sunday = '2014-07-20T14:59:59'

        start_date = datetime.strptime(
            saturday,
            "%Y-%m-%dT%H:%M:%S"
        )
        end_date = datetime.strptime(
            sunday,
            "%Y-%m-%dT%H:%M:%S"
        )

        result = calculate_work_hours(start_date, end_date)

        self.assertEquals(result, 0)

    def test_weekend_is_excluded(self):
        '''
        Ticket created on a Friday and completed on Monday
        the following week.
        '''
        friday_within_work_hours = '2014-07-25T08:59:59'
        monday_within_work_hours = '2014-07-28T11:59:59'

        start_date = datetime.strptime(
            friday_within_work_hours,
            "%Y-%m-%dT%H:%M:%S"
        )
        end_date = datetime.strptime(
            monday_within_work_hours,
            "%Y-%m-%dT%H:%M:%S"
        )
        result = calculate_work_hours(start_date, end_date)

        self.assertEquals(result, 11.0)

    def test_weekend_is_excluded_2(self):
        '''
        Ticket created on a Saturday and completed on a
        a weekday after work hours the following week.
        '''
        saturday = '2014-07-19T08:59:59'
        weekday_after_work_hours = '2014-07-22T18:59:59'

        start_date = datetime.strptime(
            saturday,
            "%Y-%m-%dT%H:%M:%S"
        )
        end_date = datetime.strptime(
            weekday_after_work_hours,
            "%Y-%m-%dT%H:%M:%S"
        )
        result = calculate_work_hours(start_date, end_date)

        self.assertEquals(result, 16.0)

    def test_weekend_is_excluded_3(self):
        '''
        Ticket created on a weekday after work hours
        and completed on a Saturday.
        '''
        weekday_after_work_hours = '2014-07-28T18:59:59'
        saturday = '2014-08-01T08:59:59'

        start_date = datetime.strptime(
            weekday_after_work_hours,
            "%Y-%m-%dT%H:%M:%S"
        )
        end_date = datetime.strptime(
            saturday,
            "%Y-%m-%dT%H:%M:%S"
        )
        result = calculate_work_hours(start_date, end_date)

        self.assertEquals(result, 24.0)

    def test_weekday_during_business_hours(self):
        '''
        Ticket created and resolved the same day during
        business hours.
        '''
        weekday_during_work_hours = '2014-07-29T09:42:25'
        weekday_during_work_hours_2 = '2014-07-29T14:35:25'

        start_date = datetime.strptime(
            weekday_during_work_hours,
            "%Y-%m-%dT%H:%M:%S"
        )
        end_date = datetime.strptime(
            weekday_during_work_hours_2,
            "%Y-%m-%dT%H:%M:%S"
        )
        result = calculate_work_hours(start_date, end_date)

        self.assertEquals(result, 4.9)

    def test_weekday_during_business_hours_2(self):
        '''
        This test covers multiple weekdays over bussiness
        hours.
        '''
        weekday_during_work_hours = '2014-07-29T09:42:25'
        weekday_during_work_hours_2 = '2014-08-01T14:05:45'

        start_date = datetime.strptime(
            weekday_during_work_hours,
            "%Y-%m-%dT%H:%M:%S"
        )
        end_date = datetime.strptime(
            weekday_during_work_hours_2,
            "%Y-%m-%dT%H:%M:%S"
        )
        result = calculate_work_hours(start_date, end_date)

        self.assertEquals(result, 28.4)

    def test_holidays_are_excluded(self):
        '''
        Test Canada day is excluded.
        '''
        weekday_during_work_hours = '2014-06-27T11:32:25'
        weekday_during_work_hours_2 = '2014-07-02T14:05:45'

        start_date = datetime.strptime(
            weekday_during_work_hours,
            "%Y-%m-%dT%H:%M:%S"
        )
        end_date = datetime.strptime(
            weekday_during_work_hours_2,
            "%Y-%m-%dT%H:%M:%S"
        )
        result = calculate_work_hours(start_date, end_date)

        self.assertEquals(result, 18.6)
