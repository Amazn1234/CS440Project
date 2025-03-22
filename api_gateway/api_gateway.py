from flask import Flask, render_template, request, redirect, jsonify
import requests

# refernce this file
app = Flask(__name__)

API_GATEWAY_PORT = 5000
DATABASE_SERVICE_URL = "http://database_service:5002"
PLANNER_SERVICE_URL = "http://planner_service:5001"

# create index route
# allow post and get for user i/o
@app.route('/', methods=['GET'])
def index():
    try:
        response = requests.get(f"{DATABASE_SERVICE_URL}/tasks")
        tasks = response.json()
    except requests.exceptions.RequestException:
        tasks = []
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    # send data to task service
    task_data = {
        "name": request.form['name'],
        "dueDate": request.form['dueDate'],
        "dueTime": request.form['dueTime'],
        "weekends": request.form.get('weekends') == "on",
        "timeToDo": int(request.form['timeToDo']),
        "workDays": int(request.form['workDays']),
        "workTime": request.form['workTime']
    }

    #verify required files are filled in

    # call planner service to gen a schedule
    try:
        schedule_response = requests.post(f"{PLANNER_SERVICE_URL}/schedule", json=task_data)
        task_data["schedule"] = schedule_response.json()["schedule"]
    except requests.exceptions.RequestException:
        task_data["schedule"] = "Error getting schedule"

    # store task in db
    try:
        requests.post(f"{DATABASE_SERVICE_URL}/tasks", json=task_data)
    except requests.exceptions.RequestException:
        return "Database service unavailable", 500 #return err and code 500
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    # delete a task, link to db service
    requests.delete(f"{DATABASE_SERVICE_URL}/tasks/{id}")
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    """
    Endpoint to update a task.
    This will send the update request to the planner service
    and to the database service to update the task record.
    """
    # Get the updated task data from the request
    updated_data = request.json
    name = updated_data.get('name')
    due_date = updated_data.get('dueDate')
    time_to_do = updated_data.get('timeToDo')
    work_days = updated_data.get('workDays')
    weekends = updated_data.get('weekends')
    work_time = updated_data.get('workTime')
    
    # Create a request payload to send to the planner service
    planner_payload = {
        "id": id,
        "dueDate": due_date,
        "workDays": work_days,
        "weekends": weekends,
        "timeToDo": time_to_do,
        "workTime": work_time
    }

    # Send the request to the planner service to update the schedule
    planner_response = requests.post(f"{PLANNER_SERVICE_URL}/{id}", json=planner_payload)

    if planner_response.status_code != 200:
        return jsonify({"error": "Failed to update task schedule"}), 500

    # Create a request payload to update the task in the database service
    database_payload = {
        "id": id,
        "name": name,
        "dueDate": due_date,
        "timeToDo": time_to_do,
        "workDays": work_days,
        "weekends": weekends,
        "workTime": work_time
    }

    # Send the request to the database service to update the task record
    db_response = requests.post(f"{DATABASE_SERVICE_URL}/{id}", json=database_payload)

    if db_response.status_code != 200:
        return jsonify({"error": "Failed to update task record"}), 500

    return jsonify({"message": "Task updated successfully"}), 200


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=API_GATEWAY_PORT, debug=True)