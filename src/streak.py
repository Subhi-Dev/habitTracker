import json
from datetime import datetime


class Streak:
    def __init__(self, entry_count=0, start_date=datetime.now(), end_date=None):
        self.entry_count = entry_count
        self.start_date = start_date
        self.end_date = end_date

    def add_entry(self):
        self.entry_count += 1

    def end_streak(self):
        self.end_date = datetime.now()

    def to_json(self):
        return {
            "entry_count": str(self.entry_count),
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if (self.end_date is not None) else "None"
        }
