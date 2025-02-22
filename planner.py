from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

# week and it's days class
class Week:
    days = { "sunday": 0, "monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0 }

def calendarPlanner(dueDateTime, workDays, weekendWork, workHours, freeHours, planner):
    # divide the estimated work hours by the days able to work
    maxHoursPerDay = workHours / (int((dueDateTime - datetime.now()).days) + 1)
    # variables that may be used if we implement checking the planner for full days or something like it
    schedList = ""
    weekList = []
    # initialize week count, used in case of tasks that span multiple weeks
    weekNumber = 0

    #for week in planner:
    #    # figure out a way to differentiate weeks
    #    schedList += task.schedule
    
    #for index in range(len(schedList) - 4):
    #    day = schedList[index] + schedList[index + 1]
    #    hours = schedList[index + 2] + schedList[index + 3]
    #    hours = int(hours)
    #    if day == "Su":
    #        weekList.append(Week)
    #        weekNumber += 1
    #    match day:
    #        case "Su":
    #            weekList[weekNumber].days["sunday"] += hours
    #        case "Mo":
    #            weekList[weekNumber].days["monday"] += hours
    #        case "Tu":
    #            weekList[weekNumber].days["tuesday"] += hours
    #        case "We":
    #            weekList[weekNumber].days["wednesday"] += hours
    #        case "Th":
    #            weekList[weekNumber].days["thursday"] += hours
    #        case "Fr":
    #            weekList[weekNumber].days["friday"] += hours
    #        case "Sa":
    #            weekList[weekNumber].days["saturday"] += hours
    
    # get today- currentDay will hold the day as we increment through the days
    currentDay = datetime.now()
    # for days in between now and due date day
    for dayIndex in range(int((dueDateTime - datetime.now()).days) + 1):
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
