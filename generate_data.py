import json
import os
from datetime import datetime, timedelta, time
import questionary

from src.habit import Habit

choice = questionary.confirm("Are you sure you want to generate new data? This will delete all existing data",
                             default=False).ask()
if choice:
    print("Generating data...")
    json_data = {
        "habits": []
    }
    dirname = os.path.dirname(__file__)
    _JSON_FILE = os.path.join(dirname, './save/user.json')

    daily_count = 0
    while daily_count < 3:
        daily_count += 1
        habit = Habit(name=f"Daily Habit {daily_count}", interval_in_days=1, timespan=timedelta(hours=1),
                      target_time=time((12 + daily_count)))
        day_count = 0
        while day_count < 30:
            day_count += 1
            habit.add_entry(datetime(2024, 2, 1, 12 + daily_count)+timedelta(days=day_count))
        json_data["habits"].append(habit.to_json())

    weekly_count = 0
    while weekly_count < 2:
        weekly_count += 1
        habit = Habit(name=f"Weekly Habit {weekly_count}", interval_in_days=7, timespan=timedelta(hours=5),
                      target_time=time((12 + weekly_count)))
        week_count = 0
        while week_count < 4:
            week_count += 1
            habit.add_entry(datetime(2024, 2, 1, 12 + weekly_count)+timedelta(weeks=week_count))
        json_data["habits"].append(habit.to_json())

    json_file = open(_JSON_FILE, "w")
    json_file.write(json.dumps(json_data))
    json_file.close()

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Done! Now run main.py to browse the data")

