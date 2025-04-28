from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from models import db, Todo
from planner import calendarPlanner, Week

# Create Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db.init_app(app)  # Link SQLAlchemy to this file

# Planner - list of Week objects
planner = [Week()]

# Create database tables if they don't exist yet
with app.app_context():
    db.create_all()

# Create index route to avoid 404
# Allow both POST (submitting a new task) and GET (viewing tasks)
@app.route('/', methods=['POST', 'GET'])
def index():
    errors = []  # List of error messages to display

    # If user submits a task (POST)
    if request.method == 'POST':
        # Get name of assignment/project
        task_name = request.form['name']

        try:
            # Get due date and time from form and combine them
            task_dueDate = request.form['dueDate']
            task_dueTime = request.form['dueTime']
            task_dueDate = datetime.strptime(task_dueDate + " " + task_dueTime, "%Y-%m-%d %H:%M:%S")
        except:
            errors.append("Error: Invalid date or time")
            return render_template("index.html", errors=errors)

        # Get checkbox for working weekends
        try:
            task_weekends = request.form['weekends']
            task_weekends = True
        except:
            task_weekends = False

        # Get estimated work hours
        try:
            task_timeToDo = int(request.form['timeToDo'])
        except:
            errors.append("Error: Please enter a valid number for time to do.")
            return render_template("index.html", errors=errors)

        # Get days user can work per week
        try:
            task_workDays = int(request.form['workDays'])
            if task_weekends:
                if task_workDays > 7 or task_workDays <= 0:
                    errors.append("Error: Please enter an amount of days 1-7")
                    return render_template("index.html", errors=errors)
            else:
                if task_workDays > 5 or task_workDays <= 0:
                    errors.append("Error: Please enter an amount of days 1-5")
                    return render_template("index.html", errors=errors)
        except:
            errors.append("Error: Please enter an integer for work days.")
            return render_template("index.html", errors=errors)

        # Get number of free hours per day
        try:
            task_workTime = request.form['workTime']
            task_workTime = datetime.strptime(task_workTime, "%H")
        except:
            errors.append("Error: Please enter a valid 2-digit hour amount")
            return render_template("index.html", errors=errors)

        # Create a schedule based on provided information
        calendarPlanner(task_dueDate, task_workDays, task_weekends, task_timeToDo, task_workTime, planner)

        # Debug: Print planner to console
        for i in planner:
            for j in i.days:
                print(j + "- " + str(i.days[j]))

        # Create new task instance
        new_task = Todo(
            name=task_name,
            dueDate=task_dueDate,
            workDays=task_workDays,
            timeToDo=task_timeToDo,
            weekends=task_weekends,
            workTime=task_workTime,
            schedule="planned"  # Placeholder, could be expanded
        )

        # Add task to database
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"{e}"

    # If request is GET (just visiting page)
    else:
        # Query database for all tasks
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks, planner=planner)

# Deletion route, expecting a task id
@app.route('/delete/<int:id>')
def delete(id):
    # Get task by id, or 404 if not found
    task_to_delete = Todo.query.get_or_404(id)

    # Delete task and commit
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

# Updating route, expecting a task id
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        # Update task name based on form input (was incorrectly labeled 'content' before)
        task.name = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating that task."

    else:
        # Render update form
        return render_template('update.html', task=task)

# Run app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
