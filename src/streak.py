from datetime import datetime


class Streak:
    """Streak class
    responsible for handling the addition of entries to a streak
    and the conversion of streaks to json
    """
    def __init__(self, entry_count=0, start_date=datetime.now(), end_date=None):
        """

        :param entry_count: integer, the number of entries a streak begins with, defaults to 0
        :param start_date: datetime, the start date of the streak, defaults to datetime.now()
        :param end_date: datetime, the end date of the streak, defaults to None
        """
        self.entry_count = entry_count
        self.start_date = start_date
        self.end_date = end_date

    def add_entry(self):
        """Adds a new entry to the streak"""
        self.entry_count += 1

    def end_streak(self):
        """Ends the streak"""
        self.end_date = datetime.now()

    def to_json(self):
        """Converts the streak instance to a json object"""
        return {
            "entry_count": str(self.entry_count),
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if (self.end_date is not None) else "None"
        }
