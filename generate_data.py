import json

import questionary

from src.habit import Habit

choice = questionary.confirm("Are you sure you want to generate new data? This will delete all existing data",
                             default=False).ask()
if choice:
    print("Generating data...")
    json_data = {
        "habits": []
    }
   
