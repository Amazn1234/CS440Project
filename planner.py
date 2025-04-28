from datetime import datetime, timedelta

# Week class - stores daily scheduled hours for a single week
class Week:
    def __init__(self):
        # Initialize dictionary for each day of the week, starting with 0 hours
        self.days = {
            "sunday": 0, "monday": 0, "tuesday": 0,
            "wednesday": 0, "thursday": 0,
            "friday": 0, "saturday": 0
        }

# Main schedule creation function
def calendarPlanner(dueDateTime, workDays, weekendWork, workHours, freeHours, planner):
    # Divide the estimated work hours by the number of days available
    maxHoursPerDay = workHours / (int((dueDateTime - datetime.now()).days) + 1)

    # Initialize current working week number
    weekNumber = 0

    # Get today's date to start scheduling from
    currentDay = datetime.now()

    # Loop through each day between now and the due date
    for dayIndex in range(int((dueDateTime - datetime.now()).days) + 1):
        # Based on current day of the week, add hours to the correct day
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

        # If Saturday, move to next week
        if currentDay.weekday() == 5:
            weekNumber += 1
            # Add a new Week object if planner doesn't have enough weeks
            if len(planner) < weekNumber + 1:
                planner.append(Week())

        # Move current day to the next day
        currentDay += timedelta(days=1)

    # No explicit return needed because planner is modified directly
