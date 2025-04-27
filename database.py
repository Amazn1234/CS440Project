from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from planner import setupPlanner

def createApp(app):
    # get db
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
    # initialize db
    db = SQLAlchemy(app)

    # database model class
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

    # connect app to the db
    with app.app_context():
        db.create_all()

    # create a planner for the app
    setupPlanner(app, db, Todo)