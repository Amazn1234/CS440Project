from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Define the URL of the Database service and planner port
DATABASE_SERVICE_URL = 'http://database_service:5002/save'
PLANNER_SERVICE_PORT = 5001

# Calculate schedule, how many hours a day and how many days to work on an assignment
def calculate_schedule(date_created, due_date, total_time, work_days, include_weekends ):
    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    schedule = {}

    time_per_day = total_time / work_days

    current_date = date_created
    while current_date <= due_date and work_days > 0:
        if include_weekends or current_date.weekday() < 5: # Remove weekends
            schedule[current_date.strftime("%Y-%m-%d")] = time_per_day
            work_days -= 1
        current_date+= timedelta(days=1)

    return schedule

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    """
    Endpoint to update a task's schedule.
    Receives task data, calculates the schedule, and sends the updated task to the database service.
    """
    data = request.json()
    due_date = data.get('dueDate')
    work_days = data.get('workDays')
    weekends = data.get('weekends')
    time_to_do = data.get('timeToDo')
    work_time = data.get('workTime')
    
    # Convert dueDate from string to datetime
    try:
        due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return jsonify({"error": f"Invalid due date format: {e}"}), 400

    # Calculate the schedule based on the provided data
    schedule = calculate_schedule(datetime.today(), due_date, work_time, work_days, weekends)

    # Prepare the data for sending to the database service
    task_data = {
        "id": id,
        "dueDate": due_date,
        "workDays": work_days,
        "weekends": weekends,
        "timeToDo": time_to_do,
        "workTime": work_time,
        "schedule": json.dumps(schedule)  # Convert the schedule to a JSON string
    }

    # Send the task data to the database service to save
    response = requests.post(DATABASE_SERVICE_URL, json=task_data)

    if response.status_code != 200:
        return jsonify({"error": "Failed to update task in the database"}), 500

    return jsonify({"message": "Task updated successfully"}), 200

@app.route('/create', methods=['POST'])
def create_task():
    # Endpoint to create a new task, calculate the schedule, and save it to the database service.

    # get task data from api_gateway
    data = request.json
    name = data.get('name')
    due_date = data.get('dueDate')
    work_days = data.get('workDays')
    weekends = data.get('weekends')
    time_to_do = data.get('timeToDo')
    work_time = data.get('workTime')

    # Convert dueDate from string to datetime
    try:
        due_date = datetime.strptime(due_date, "%MM-%DD-%YYYY %H:%M:%S")
    except Exception as e:
        return jsonify({"error": f"Invalid due date format: {e}"}), 400

    # Calculate the schedule for the new task
    schedule = calculate_schedule(due_date, work_days, weekends, time_to_do, work_time)

    # Prepare the task data
    task_data = {
        "name": name,
        "dueDate": due_date,
        "workDays": work_days,
        "weekends": weekends,
        "timeToDo": time_to_do,
        "workTime": work_time,
        "schedule": json.dumps(schedule)  # Convert schedule to a JSON string
    }

    # Send the new task data to the database service to save it
    response = requests.post(DATABASE_SERVICE_URL, json=task_data)

    if response.status_code != 200:
        return jsonify({"error": "Failed to create task in the database"}), 500

    return jsonify({"message": "Task created successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PLANNER_SERVICE_PORT)
