import os
import json

from datetime import datetime, timedelta, date

from streak import Streak


class Habit:
    dirname = os.path.dirname(__file__)
    _JSON_FILE = os.path.join(dirname, '../save/user.json')

    def __init__(self, name: str, created_at=datetime.now(), last_entry_date=None,
                 interval_in_days: int = 1, target_time=datetime.now().time(), timespan=timedelta(hours=1)):
        self.name = name
        self.created_at = created_at
        self.interval_in_days = interval_in_days
        self.last_entry_date = last_entry_date
        self.streaks = []
        self.target_time = target_time
        self.timespan = timespan

    def add_entry(self):
        """Adds a new entry to the habit."""
        if datetime.combine(date.today(), self.target_time) - datetime.now() < self.timespan:
            print("You can not check-off now, you must check-off your habit within "
                  + str(self.timespan) + " of " + str(self.target_time))
        elif self.last_entry_date - datetime.now() <= timedelta(days=self.interval_in_days):
            print("You checked-off your habit!, see you next time")
            self.streaks[-1].add_entry()
            self.last_entry_date = datetime.now()
        else:
            print("You missed your streak, try doing better next time")
            self.streaks[-1].end_streak()
            self.streaks.append(Streak())
        print("Current Streak: " + str(self.streaks[-1].entryCount))

    def to_json(self):
        """Converts the habit instance to a JSON object"""
        return {
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "interval_in_days": str(self.interval_in_days),
            "last_entry_date": str(self.last_entry_date),
            "streaks": [streak.to_json() for streak in self.streaks],
            "target_time": str(self.target_time),
            "timespan": str(self.timespan)
        }

    @classmethod
    def interval_to_periodicity(cls, interval):
        if interval == 1:
            return "Daily"
        elif interval == 7:
            return "Weekly"
        else:
            return f"{str(interval)} days"

    @classmethod
    def from_json(cls, json_data):
        """Converts a JSON string to a Habit Object"""
        data = json.loads(json_data)
        habit = cls(name=data["name"], created_at=data["created_at"], interval_in_days=data["interval_in_days"],
                    last_entry_date=data["last_entry_date"], target_time=data["target_time"], timespan=data["timespan"])
        habit.streaks = [Streak(entry_count=streak.entry_count, start_date=streak.start_date, end_date=streak.end_date)
                         for streak in data["streaks"]]
        return habit

    @classmethod
    def get_all_data(cls):
        """Returns an array of all habits"""
        json_file = open(cls._JSON_FILE, "r")
        json_data = json.loads(json_file.read())
        json_file.close()
        return json_data

    def add_habit_to_json(self):
        """Adds the habit object to the JSON file"""
        json_data = self.get_all_data()
        json_data["habits"].append(self.to_json())
        json_file = open(self._JSON_FILE, "w")
        json_file.write(json.dumps(json_data))
        json_file.close()

    @classmethod
    def validate_habit(cls, value):
        """Validates the new habit name to prevent name duplicates"""
        data = cls.get_all_data()
        for habit in data["habits"]:
            if habit["name"] == value:
                return False
        return True

    @classmethod
    def habit_search(cls, name):
        """Search for habit name and return the habit object"""
        json_data = cls.get_all_data()
        for habit in json_data["habits"]:
            if habit["name"] == name:
                return habit
        return False

    @classmethod
    def habit_update(cls, old_habit, habit):
        """Updates the habit from a habit object input"""
        data = cls.get_all_data()
        data["habits"].remove(old_habit)
        data["habits"].append(habit)
        json_file = open(cls._JSON_FILE, "w")
        json_file.write(json.dumps(data))
        json_file.close()


    def return_largest_streak(self):
        """Returns the largest streak that the habit has"""
        return max(streak.entryCount for streak in self.streaks)
