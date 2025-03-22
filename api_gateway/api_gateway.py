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
        "name": request.form['dueDate'] + " " + requests.form['dueTime'],
        "timeToDo": int(request.form['timeToDo']),
        "workDays": int(request.form['workDays']),
        "weekends": request.form.get('weekends') == "on",
        "workTime": request.form['workTime']
    }

    # call planner service to gen a schedule
    try:
        schedule_response = requests.post(f"{PLANNER_SERVICE_URL}/schedule", json=task_data)
        task_data["schedule"] = schedule_response.son()["schedule"]
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


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=API_GATEWAY_PORT, debug=True)