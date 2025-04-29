from datetime import datetime, timedelta

# Week class - stores daily scheduled hours for a week
class Week:
    def __init__(self):
        self.days = {
            "sunday": 0, "monday": 0, "tuesday": 0,
            "wednesday": 0, "thursday": 0,
            "friday": 0, "saturday": 0
        }

# Function to create a schedule based on provided task information
def calendarPlanner(dueDateTime, workDays, weekendWork, workHours, freeHours, planner):
    # Divide the estimated work hours by the number of days until the due date
    maxHoursPerDay = workHours / (int((dueDateTime - datetime.now()).days) + 1)

    # Initialize current working week number
    weekNumber = 0

    # Start from today
    currentDay = datetime.now()

    # Loop through each day between now and due date
    for dayIndex in range(int((dueDateTime - datetime.now()).days) + 1):
        # Determine what day of the week it is, and add hours
        match currentDay.weekday():
            case 0:
                planner[weekNumber].days["monday"] += maxHoursPerDay
            case 1:
                planner[weekNumber].days["tuesday"] += maxHoursPerDay
            case 2:
                planner[weekNumber].days["wednesday"] += maxHoursPerDay
            case 3:
                planner[weekNumber].days["thursday"] += maxHoursPerDay
            case 4:
                planner[weekNumber].days["friday"] += maxHoursPerDay
            case 5:
                planner[weekNumber].days["saturday"] += maxHoursPerDay
            case 6:
                planner[weekNumber].days["sunday"] += maxHoursPerDay

        # After Saturday, add a new week if needed
        if currentDay.weekday() == 5:
            weekNumber += 1
            if len(planner) < weekNumber + 1:
                planner.append(Week())

        # Move to next day
        currentDay += timedelta(days=1)
