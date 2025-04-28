from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy (database object)
db = SQLAlchemy()

# Todo model class - defines the structure of a task in the database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(50), nullable=False)  # Task name
    dueDate = db.Column(db.DateTime, nullable=False)  # Task due date/time
    timeToDo = db.Column(db.Integer, nullable=False)  # Estimated hours needed
    workDays = db.Column(db.Integer, nullable=False)  # Days available to work
    weekends = db.Column(db.Boolean, nullable=False)  # Whether user can work weekends
    workTime = db.Column(db.DateTime, nullable=False)  # Max work hours per day
    schedule = db.Column(db.String(50))  # Schedule info (currently simple)
    date_created = db.Column(db.DateTime, default=datetime.now)  # Timestamp of creation

    # Display format for debugging
    def __repr__(self):
        return '<Task %r>' % self.id
