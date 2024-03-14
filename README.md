# Python Habit Tracker
A Python program with a Command-line interface that allows Habit tracking. Easily create and check-off daily and weekly habits.

## Features

- Create Daily and Weekly habits
- Edit habits
- Analyze habits

## Requirements

- Python v3.12 minimum


## Installation

Clone the repository by downloading it and run a terminal
```shell
pip install -r requirements
```

## Usage

Run the following command in the project root directory (The same directory for this README)
```shell
python main.py
```
Note that you must run this in an interactive terminal

You will be presented with a number of actions to perform, You can:
    
- View all habits: Shows all active habits
- Add a habit: Creates a new habit
- Edit a habit: Change a specific property of a habit
- Check-off a habit: adds an entry to a selected habit 
- Analyze habits: Gives a choice of interesting stats to calculate

Then the application will guide you through the rest of the setup process

### Sample Data Generation

If you cloned the repository your ```save/user.json``` file must look like this

```json
{
  "habit": []
}
```

To generate the sample data proceed to run the following command in the project root
```shell
python generate_data.py
```
This will generate 5 habits (3 daily and 2 weekly) with 4 weeks of data each

## Testing

If you want to contribute or modify to this application, use the following command to automatically check basic functionality
```shell
pytest tests
```