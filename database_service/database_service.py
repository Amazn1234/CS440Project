from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# reference this file
app = Flask(__name__)
# get db
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
# initialize db
db = SQLAlchemy(app)

# database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    dueDate = db.Column(db.DateTime, nullable=False)
    timeToDo = db.Column(db.Integer, nullable=False)
    workDays = db.Column(db.Integer, nullable=False)
    weekends = db.Column(db.Boolean, nullable=False)
    workTime = db.Column(db.DateTime, nullable=False)
    schedule = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dueDate': self.dueDate.isoformat(),  # Convert datetime to string
            'timeToDo': self.timeToDo,
            'workDays': self.workDays,
            'weekends': self.weekends,
            'workTime': self.workTime.isoformat(),  # Convert datetime to string
            'schedule': self.schedule,
            'date_created': self.date_created
        }
    
    
# route for adding a task
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    errors = []

    # if method is POST(adding a task)
    if request.method == 'POST':
        task_data = request.json

        task_name = task_data['name']

        try:
            # get due date and time
            task_dueDate = task_data['dueDate']
            task_dueTime = task_data['dueTime']
            # turn into a datetime object
            task_dueDate = datetime.strptime(task_dueDate + " " + task_dueTime, "%Y-%m-%d %H:%M:%S")
        # if failure to do so, send error
        except:
            errors.append("Error: Invalid date or time")
            return {"errors": errors}, 400
        
        # get if user is willing to work weekends
        # set checkbox response as boolean
        task_weekends = bool(task_data['weekends'])
        
        task_timeToDo = int(task_data['timeToDo'])
        
        # get the days of the week to work
        try:
            task_workDays = int(task_data['workDays'])
            # check if valid amount of days- if not, send error
            if task_weekends:
                if task_workDays > 7 or task_workDays <= 0:
                    errors.append("Error: Please enter an amount of days 1-7")
                    return {"errors": errors}, 400
            else:
                if task_workDays > 5 or task_workDays <= 0:
                    errors.append("Error: Please enter an amount of days 1-5")
                    return {"errors": errors}, 400
        # if not an int, send error
        except:
            errors.append("Error: Please enter an integer")
            return {"errors": errors}, 400
        
        # get how much time user can work per day
        task_workTime = task_data['workTime']
        # turn into a datetime object
        try:
            task_workTime = datetime.strptime(task_workTime, "%H")
        # if failure to do so, send error
        except:
            errors.append("Error: Please enter a valid 2-digit hour amount")
            return {"errors": errors}, 400
        
        # get the schedule added by the planner microservice
        task_schedule = task_data["schedule"]
        
        new_task = Todo(name=task_name, dueDate=task_dueDate, workDays=task_workDays, timeToDo=task_timeToDo,
                         weekends=task_weekends, workTime=task_workTime, schedule=task_schedule)
        
        # add task to db and commit
        try:
            db.session.add(new_task)
            db.session.commit()
            return {"message": "Task added successfully"}, 201
        # if error encountered, return error
        except Exception as e:
            # rollback just to be safe
            db.session.rollback()
            # send an error back
            return {"error": "Failed to add task", "details": str(e)}, 500
    
    # else is a GET request
    else:
        # query database for all tasks
        tasks = Todo.query.order_by(Todo.date_created).all()
        # convert tasks to a list of dictionaries
        return {"tasks": [task.to_dict() for task in tasks]}
    
# route for deleting a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    # get the task to delete by id
    task_to_delete = Todo.query.get(id)

    # if nothing found, return an error
    if not task_to_delete:
        return {"error": "Task not found"}, 404

    # try to commit the deletion to the db
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        # return a success message
        return {"message": "Task deleted successfully"}, 200
    # otherwise, rollback changes and return an error
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to delete task", "details": str(e)}, 500
    
# route for updating a task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    # get the task to update by id
    task_to_update = Todo.query.get(id)

    # if task not found, return an error
    if not task_to_update:
        return {"error": "Task not found"}, 404
    
    # try to update task
    try:
        # get the stream of json data
        task_data = request.json

        # check if an attribute is being updated, if so, update the original task with the
        # new value
        if "name" in task_data:
            task_to_update.name = task_data["name"]
        if "dueDate" in task_data and "dueTime" in task_data:
            task_to_update.dueDate = datetime.strptime(task_data["task_dueDate"] + " " + task_data["task_dueTime"], "%Y-%m-%d %H:%M:%S")
        if "timeToDo" in task_data:
            task_to_update.timeToDo = task_data["timeToDo"]
        if "workDays" in task_data:
            task_to_update.workDays = task_data["workDays"]
        if "weekends" in task_data:
            task_to_update.weekends = task_data["weekends"]
        if "workTime" in task_data:
            task_to_update.workTime = task_data["workTime"]
        if "schedule" in task_data:
            task_to_update.schedule = task_data["schedule"]
        
        # commit the changes
        db.session.commit()
        # return a success message
        return {"message": "Task updated successfully", "task": task_to_update.to_dict()}, 200
    
    # if an error occurs
    except Exception as e:
        # rollback changes and return an error
        db.session.rollback()
        return {"error": "Failed to update task", "details": str(e)}, 500

# run the service
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)