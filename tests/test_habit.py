from datetime import datetime, time, timedelta

import pytest

from src.habit import Habit


class TestHabit:
    def setup_method(self):
        self.habit = Habit(name="Daily Test", timespan=timedelta(hours=5), target_time=time(hour=12))
        self.habit_weekly = Habit(name="Weekly Test", timespan=timedelta(hours=12), target_time=time(hour=12),
                                  interval_in_days=7)

    def test_single_date(self):
        # Test Checking-off a single time
        self.habit.add_entry(datetime(2023, 1, 11, 12))
        assert self.habit.streaks[-1].entry_count == 1

    def test_multiple_dates(self):
        # Test Checking-off multiple dates and checking the streak functionality
        self.habit.add_entry(datetime(2023, 2, 11, 12))  # This should not count towards the streak
        self.habit.add_entry(datetime(2023, 2, 14, 11))
        self.habit.add_entry(datetime(2023, 2, 15, 14, 30))
        self.habit.add_entry(datetime(2023, 2, 16, 12))
        assert self.habit.streaks[-1].entry_count == 3

    def test_analyze_max_streak(self):
        # Test analyzing the max streak feature
        self.habit.add_entry(datetime(2023, 3, 14, 12))
        self.habit.add_entry(datetime(2023, 3, 15, 7, 30))  # Tests extreme check-off cases
        self.habit.add_entry(datetime(2023, 3, 16, 16, 30))
        self.habit.add_entry(datetime(2023, 3, 17, 10, 1))
        self.habit.add_entry(datetime(2023, 3, 18, 12))
        assert self.habit.return_largest_streak == 5

    def test_weekly_habit(self):
        # Tests checking-off weekly habits
        self.habit_weekly.add_entry(datetime(2023, 3, 7, 12))  # Doesn't count towards the streak
        self.habit_weekly.add_entry(datetime(2023, 3, 16, 14, 25))
        self.habit_weekly.add_entry(datetime(2023, 3, 21, 12))
        self.habit_weekly.add_entry(datetime(2023, 3, 28, 10, 20))
        assert self.habit_weekly.streaks[-1].entry_count == 3

    def teardown_method(self):
        # Clean up the habit instance
        del self.habit
        del self.habit_weekly


pytest.main()
