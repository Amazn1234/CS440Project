from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from planner import *

# refernce this file
app = Flask(__name__)
# get db
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
# initialize db
db = SQLAlchemy(app)

class Week:
    days = { "sunday": 0, "monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0 }

# planner
planner = []
planner.append(Week)

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

with app.app_context():
    db.create_all()

# create index route to avoid 404
# allow post and get for user i/o
@app.route('/', methods=['POST', 'GET'])
def index():
    errors = []
    # if request is POST
    if request.method == 'POST':
        # get contents of html's post form
        # get name of assignment/project
        task_name = request.form['name']

        try:
            # get due date and time
            task_dueDate = request.form['dueDate']
            task_dueTime = request.form['dueTime']
            # turn into a datetime object
            task_dueDate = datetime.strptime(task_dueDate + " " + task_dueTime, "%Y-%m-%d %H:%M:%S")
        # if failure to do so, restart form
        except:
            errors.append("Error: Invalid date or time")
            return render_template("index.html", errors=errors)
        
        # get if user is willing to work weekends
        # set checkbox response as boolean
        try:
            task_weekends = request.form['weekends']
            task_weekends = True
        # if checkbox not found, means user did not check yes, set False
        except:
            task_weekends = False
        
        task_timeToDo = int(request.form['timeToDo'])
        
        # get the days of the week to work
        try:
            task_workDays = int(request.form['workDays'])
            # check if valid amount of days- if not, restart form
            if task_weekends:
                if task_workDays > 7 or task_workDays <= 0:
                    errors.append("Error: Please enter an amount of days 1-7")
                    return render_template("index.html", errors=errors)
            else:
                if task_workDays > 5 or task_workDays <= 0:
                    errors.append("Error: Please enter an amount of days 1-5")
                    return render_template("index.html", errors=errors)
        # if not an int, restart form
        except:
            errors.append("Error: Please enter an integer")
            return render_template("index.html", errors=errors)
        
        # get how much time user can work per day
        task_workTime = request.form['workTime']
        # turn into a datetime object
        try:
            task_workTime = datetime.strptime(task_workTime, "%H")
        # if failure to do so, restart form
        except:
            errors.append("Error: Please enter a valid 2-digit hour amount")
            return render_template("index.html", errors=errors)
        
        task_schedule = calendarPlanner(task_dueDate, task_workDays, task_weekends, task_timeToDo, task_workTime, planner)
        for i in planner:
            for j in i.days:
                print(j + "- " + str(i.days[j]))
        # create new task
        new_task = Todo(name=task_name, dueDate=task_dueDate, workDays=task_workDays, timeToDo=task_timeToDo,
                         weekends=task_weekends, workTime=task_workTime, schedule=task_schedule)
        
        # add task to db and commit, then redirect to main page
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        # if error encountered, return error
        except Exception as e:
            return f"{e}"
        
    # if not
    else:
        # query database for all tasks
        tasks = Todo.query.order_by(Todo.date_created).all()
        # show the main page
        return render_template("index.html", tasks=tasks, planner=planner)

# deletion route, will be expecting a task id
@app.route('/delete/<int:id>')
def delete(id):
    # get task by id, or 404
    task_to_delete = Todo.query.get_or_404(id)

    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
    
# updating route, will be expecting a task id
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error in updating that task."

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)