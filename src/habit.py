import os
import json

from datetime import datetime, timedelta

from src.streak import Streak


class Habit:
    """The main habit class
    is responsible for the management of habits conversion to json except for streaks
    and the file saving mechanism
    """
    dirname = os.path.dirname(__file__)
    _JSON_FILE = os.path.join(dirname, '../save/user.json')

    def __init__(self, name: str, created_at=datetime.now(), last_entry_date=None,
                 interval_in_days: int = 1, target_time=datetime.now().time(), timespan=timedelta(hours=1)):
        """
        Initializes the Habit
        :param name: string
        :param created_at: datetime.now()
        :param last_entry_date: None or datetime
        :param interval_in_days: int, defaults to 1
        :param target_time: time
        :param timespan: timedelta (use with hours only)
        """
        self.name = name
        self.created_at = created_at
        self.interval_in_days = interval_in_days
        self.last_entry_date = last_entry_date
        self.streaks = []
        self.target_time = target_time
        self.timespan = timespan

    def add_entry(self, entry_date=datetime.now()):
        """Adds a new entry to the habit.
        :param entry_date: datetime, used for overriding the entry date in testing
        ,defaults to datetime.now()
        """
        if abs(datetime.combine(entry_date.date(), self.target_time) - entry_date) > self.timespan:
            print("You can not check-off now, you must check-off your habit within "
                  + str(self.timespan.seconds // 3600) + " hours of " + str(self.target_time))
        elif self.last_entry_date is None:
            print("Congrats! Your habit has been checked-off for the first time")
            streak = Streak(entry_count=1, start_date=entry_date)
            self.streaks.append(streak)
            self.last_entry_date = entry_date
        elif entry_date.date() - self.last_entry_date.date() <= (timedelta(days=self.interval_in_days)):
            print("You checked-off your habit!, see you next time")
            self.streaks[-1].add_entry()
            self.last_entry_date = entry_date
            print("Current Streak: " + str(self.streaks[-1].entry_count))
        else:
            print("You missed your streak, try doing better next time")
            self.last_entry_date = entry_date
            self.streaks[-1].add_entry()
            self.streaks[-1].end_streak()
            self.streaks.append(Streak(entry_count=1, start_date=entry_date))

    def to_json(self):
        """Converts the habit instance to a JSON object"""
        return {
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "interval_in_days": str(self.interval_in_days),
            "last_entry_date": "None" if self.last_entry_date is None else self.last_entry_date.isoformat(),
            "streaks": [streak.to_json() for streak in self.streaks],
            "target_time": self.target_time.isoformat(),
            "timespan": str(self.timespan.seconds // 3600)
        }

    @classmethod
    def interval_to_periodicity(cls, interval):
        """Converts the Interval in days to a Periodicity
        Example: interval of 1 day is a periodicity of "Daily"
        :param interval: integer Interval in days
        """
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
        habit = cls(name=data["name"], created_at=datetime.fromisoformat(data["created_at"]),
                    interval_in_days=int(data["interval_in_days"]),
                    last_entry_date=None if data["last_entry_date"] == "None"
                    else datetime.fromisoformat(data["last_entry_date"]),
                    target_time=datetime.strptime(data["target_time"], "%H:%M:%S").time(),
                    timespan=timedelta(hours=int(data["timespan"])))
        habit.streaks = [Streak(entry_count=int(streak["entry_count"]),
                                start_date=datetime.fromisoformat(streak["start_date"]),
                                end_date=None if streak["end_date"] == "None"
                                else datetime.fromisoformat(streak["end_date"])) for streak in data["streaks"]]
        return habit

    @classmethod
    def get_all_data(cls):
        """Returns an array of all habits"""
        json_file = open(cls._JSON_FILE, "r")
        json_data = json.loads(json_file.read())
        json_file.close()
        return json_data

    def add_habit_to_json(self):
        """Adds the habit instance to the JSON file"""
        json_data = self.get_all_data()
        json_data["habits"].append(self.to_json())
        json_file = open(self._JSON_FILE, "w")
        json_file.write(json.dumps(json_data))
        json_file.close()

    @classmethod
    def validate_habit(cls, value):
        """Validates the new habit name to prevent name duplicates
        :param value: The habit name to validate
        """
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
        """Updates the habit from an old habit and a new habit object input"""
        data = cls.get_all_data()
        data["habits"].remove(old_habit)
        data["habits"].append(habit)
        json_file = open(cls._JSON_FILE, "w")
        json_file.write(json.dumps(data))
        json_file.close()

    def return_largest_streak(self):
        """Returns the largest streak that the habit has"""
        if not self.streaks:
            return 0
        return max(streak.entry_count for streak in self.streaks)
