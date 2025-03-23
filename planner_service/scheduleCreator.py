from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

# week and it's days class
class Week:
    def __init__(self):
        days = { "sunday": 0, 
                "monday": 0, 
                "tuesday": 0, 
                "wednesday": 0, 
                "thursday": 0, 
                "friday": 0, 
                "saturday": 0 
                }
    def to_dict(self):
        return self.days

def calendarPlanner(dueDateTime, workDays = 1, weekendWork = False, workHours = 0, freeHours = 1):
    # divide the estimated work hours by the days able to work
    maxHoursPerDay = workHours / (int((dueDateTime - datetime.now()).days) + 1)
    # variables that may be used if we implement checking the planner for full days or something similar
    # schedList = ""
    # weekList = []

    # initialize week count, used in case of tasks that span multiple weeks
    weekNumber = 0
    planner = [Week()]
    
    # get today- currentDay will hold the day as we increment through the days
    currentDay = datetime.now()
    # for days in between now and due date day
    for dayIndex in range(int((dueDateTime - datetime.now()).days) + 1):

        day_name = currentDay.strftime("%A").lower() # day name
        if day_name in planner[weekNumber].days: #if valud day
            planner[weekNumber].days[day_name] += maxHoursPerDay

        if currentDay.weekday() == 5:
            weekNumber += 1
            planner.append(Week())
        
        # increment current day
        currentDay += timedelta(days=1)
    
    return json.dumps([week.to_dict() for week in planner], indent = 2)
"""
        # get the day of the week, add the time to the day
        match (currentDay.weekday()):
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

        # if a new week is coming, change weeks and add a week to planner if needed
        if (currentDay.weekday()) == 5:
            weekNumber += 1
            if len(planner) < weekNumber + 1:
                planner.append(Week)
                
        # add a day to currentDay
        currentDay += timedelta(days=1)

    return planner
"""