from django.test import TestCase
from habit_app.utils import hours_since_time, compare_utc, calculate_streak
import time
from datetime import datetime

# Create your tests here.
class TestTimeFunctions(TestCase):

    def test_hours_since_time(self):
        # Mocking current time to a fixed value for testing
        fixed_time = datetime(2023, 9, 28, 14, 17, 0)
        time.time = lambda: fixed_time.timestamp()
        self.assertEqual(hours_since_time('2023-09-28 13:17:00'), 1)
        self.assertEqual(hours_since_time('2023-09-27 14:17:00'), 24)
        self.assertEqual(hours_since_time('2023-09-26 14:17:00'), 48)

    def test_compare_utc(self):
        self.assertEqual(compare_utc('2023-09-28 13:17:00', '2023-09-28 14:17:00'), 1)
        self.assertEqual(compare_utc('2023-09-27 14:17:00', '2023-09-28 14:17:00'), 24)
        self.assertEqual(compare_utc('2023-09-26 14:17:00', '2023-09-28 14:17:00'), 48)

    def test_calculate_streak(self):
        utc_list = ["2023-09-20 13:17:00", "2023-09-21 13:17:00", "2023-09-22 13:17:00", "2023-09-23 13:17:00", "2023-09-24 13:17:00"]
        self.assertEqual(calculate_streak(utc_list), 96)  # Assuming the output is in hours
        # Additional test cases
        utc_list_2 = ["2023-09-22 13:17:00"]
        self.assertEqual(calculate_streak(utc_list_2), 0)  # Edge case with a single date
        utc_list_3 = []  # Edge case with no dates
        self.assertEqual(calculate_streak(utc_list_3), 0)

        # Additional test cases with varying date intervals
        utc_list_4 = ["2023-09-22 13:17:00", "2023-09-23 14:17:00", "2023-09-24 15:17:00",
                      "2023-09-25 13:17:00", "2023-09-26 13:17:00"]
        self.assertEqual(calculate_streak(utc_list_4), 96)