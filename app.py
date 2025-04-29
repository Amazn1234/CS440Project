from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from services.databaseService import db, Todo  # Import database service
from services.plannerService import calendarPlanner, Week  # Import planner service

# Create Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db.init_app(app)  # Initialize db with app

# Planner - list of Week objects
planner = [Week()]

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Home route (main page) - handles creating and displaying tasks
@app.route('/', methods=['POST', 'GET'])
def index():
    errors = []  # List of error messages to show

    if request.method == 'POST':
        # Get task name
        task_name = request.form['name']

        try:
            # Get due date and time and combine
            task_dueDate = request.form['dueDate']
            task_dueTime = request.form['dueTime']
            task_dueDate = datetime.strptime(task_dueDate + " " + task_dueTime, "%Y-%m-%d %H:%M:%S")
        except:
            errors.append("Error: Invalid date or time")
            return render_template("index.html", errors=errors)

        # Get weekends availability (checkbox)
        try:
            task_weekends = request.form['weekends']
            task_weekends = True
        except:
            task_weekends = False

        # Get total time needed to complete task
        try:
            task_timeToDo = int(request.form['timeToDo'])
        except:
            errors.append("Error: Please enter a valid number for time to do.")
            return render_template("index.html", errors=errors)

        # Get number of working days
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

        # Get available work hours per day
        try:
            task_workTime = request.form['workTime']
            task_workTime = datetime.strptime(task_workTime, "%H")
        except:
            errors.append("Error: Please enter a valid 2-digit hour amount")
            return render_template("index.html", errors=errors)

        # Call planner service to create a schedule
        calendarPlanner(task_dueDate, task_workDays, task_weekends, task_timeToDo, task_workTime, planner)

        # Debug: Print planner in console
        for i in planner:
            for j in i.days:
                print(j + "- " + str(i.days[j]))

        # Create new Todo object
        new_task = Todo(
            name=task_name,
            dueDate=task_dueDate,
            workDays=task_workDays,
            timeToDo=task_timeToDo,
            weekends=task_weekends,
            workTime=task_workTime,
            schedule="planned"  # Simple placeholder
        )

        # Save task to database
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"{e}"

    else:
        # GET request - Show tasks
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks, planner=planner)

# Route to delete a task
@app.route('/delete/<int:id>')
def delete(id):
    # Get task by id or return 404
    task_to_delete = Todo.query.get_or_404(id)

    # Delete and commit
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

# Route to update a task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        # Update task name based on form input
        task.name = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating that task."

    else:
        return render_template('update.html', task=task)

# Main runner
if __name__ == "__main__":
    app.run(debug=True)
