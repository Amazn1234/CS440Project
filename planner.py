from routes import createRoutes

def setupPlanner(app, db, Todo):
    # week object
    class Week:
        days = { "sunday": 0, "monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0 }

    # planner
    planner = []
    planner.append(Week)

    # set up flask routes
    createRoutes(app, db, Todo, planner)