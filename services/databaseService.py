from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy object
db = SQLAlchemy()

# Todo model class - describes the database structure
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each task
    name = db.Column(db.String(50), nullable=False)  # Name of the task
    dueDate = db.Column(db.DateTime, nullable=False)  # Due date/time
    timeToDo = db.Column(db.Integer, nullable=False)  # Estimated time to complete
    workDays = db.Column(db.Integer, nullable=False)  # Days available to work
    weekends = db.Column(db.Boolean, nullable=False)  # Can work weekends?
    workTime = db.Column(db.DateTime, nullable=False)  # Max work time/day
    schedule = db.Column(db.String(50))  # Scheduled output (simple for now)
    date_created = db.Column(db.DateTime, default=datetime.now)  # Auto-created date

    # How the object shows when printed
    def __repr__(self):
        return '<Task %r>' % self.id
