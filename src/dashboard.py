import os

import questionary
from datetime import datetime

from habit import Habit


def validate_time(value):
    try:
        return bool(datetime.strptime(value, "%I:%M %p"))
    except ValueError:
        return False


def validate_integer(value):
    try:
        return bool(int(value))
    except ValueError:
        return False


def main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    choice = questionary.select(
        "What would you like to do?",
        choices=[
            "View all habits",
            "Add a habit",
            "Edit a habit",
            "Analyze habits",
            "Exit"
        ]
    ).ask()
    if choice == "View all habits":
        data = Habit.get_all_data()
        print("Habits:")
        for habit in data["habits"]:
            periodicity = Habit.interval_to_periodicity(int(habit["interval_in_days"]))
            data["target_time"] = datetime.strptime(habit["target_time"], "%H:%M:%S").strftime('%I:%M %p')
            print(f"Habit: {habit["name"]} | Periodicity: {periodicity} | Target Time: {data['target_time']}")
        questionary.press_any_key_to_continue().ask()
        main_menu()
    elif choice == "Add a habit":
        name = questionary.text("What is the Habit's name?",
                                validate=lambda value: Habit.validate_habit(value)).ask()
        periodicity = questionary.select("What is the periodicity of the habit?", ["Daily", "Weekly"]).ask()
        interval_in_days = 1 if periodicity == "Daily" else 7
        habit_time = questionary.text("What time would you like to do the habit? (ex: 9:00 PM)",
                                      validate=lambda value: validate_time(value)).ask()
        timespan = questionary.text("Within how many hours will you be checking-off?",
                                    validate=lambda value: validate_integer(value),
                                    default="1").ask()
        if name and interval_in_days and habit_time and timespan:
            habit = Habit(name=name, interval_in_days=interval_in_days,
                          target_time=datetime.strptime(habit_time, "%I:%M %p").time(), timespan=int(timespan))
            habit.add_habit_to_json()
            print("The habit has been added successfully!")
        else:
            print("You might have missed one of the prompts, Please try again")
        questionary.press_any_key_to_continue().ask()
        main_menu()
    elif choice == "Edit a habit":
        data = Habit.get_all_data()
        chosen_habit = questionary.select("Choose a habit to edit:", [habit["name"] for habit in data["habits"]]).ask()
        habit = Habit.habit_search(chosen_habit)
        old_habit = Habit.habit_search(chosen_habit)
        param = questionary.select("What do you want to edit?", [
            "Name",
            "Periodicity",
            "Habit Time",
            "Timespan"
        ]).ask()
        if param == "Name":
            habit["name"] = questionary.text("New name:").ask()
        elif param == "Periodicity":
            periodicity = questionary.select("New periodicity:", ["Daily", "Weekly"]).ask()
            habit["interval_in_days"] = 1 if periodicity == "Daily" else 7
        elif param == "Habit Time":
            habit_time = questionary.text("New habit time:", validate=lambda value: validate_time(value)).ask()
            habit["target_time"] = datetime.strptime(habit_time, "%I:%M %p")
        elif param == "Timespan":
            habit_timespan = questionary.text("New timespan:", validate=lambda value: validate_integer(value)).ask()
            habit["timespan"] = habit_timespan
        else:
            print("You must select a parameter to modify")
        Habit.habit_update(old_habit, habit)
        questionary.press_any_key_to_continue().ask()
        main_menu()
    elif choice == "Analyze habits":
        analysis_choice = questionary.select("What would you like to analyze?", [
            "Habit with the longest streak",
            "Habit grouped based on periodicity",
            "Habit ordered based on streak"
        ])
        if analysis_choice == "Habit with the longest streak"
    elif choice == "Exit":
        exit()


main_menu()
