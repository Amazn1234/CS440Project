from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class Week:
    def __init__(self):
        self.days = { "sunday": 0, "monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0 }

def calenderPlanner(dueDateTime, workDays, weekendWork, workHours, freeHours, database):
    maxHoursPerDay = workHours / workDays
    tasks = database.query.order_by(database.dueDate).all()
    schedList = ""
    weekList = []
    weekNumber = 0

    for task in tasks:
        # figure out a way to differentiate weeks
        schedList += task.schedule
    
    for index in range(len(schedList) - 4):
        day = schedList[index] + schedList[index + 1]
        hours = schedList[index + 2] + schedList[index + 3]
        hours = int(hours)
        if day == "Su":
            weekList.append(Week)
            weekNumber += 1
        match day:
            case "Su":
                weekList[weekNumber].days["sunday"] += hours
            case "Mo":
                weekList[weekNumber].days["monday"] += hours
            case "Tu":
                weekList[weekNumber].days["tuesday"] += hours
            case "We":
                weekList[weekNumber].days["wednesday"] += hours
            case "Th":
                weekList[weekNumber].days["thursday"] += hours
            case "Fr":
                weekList[weekNumber].days["friday"] += hours
            case "Sa":
                weekList[weekNumber].days["saturday"] += hours