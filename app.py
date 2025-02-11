from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# refernce this file
app = Flask(__name__)
# get db
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
# initialize db
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all()

# create index route to avoid 404
# allow post and get for user i/o
@app.route('/', methods=['POST', 'GET'])
def index():
    # if request is POST
    if request.method == 'POST':
        # get contents of html's post form
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error encountered while adding your task."
        
    # if not
    else:
        # query database for all tasks
        tasks = Todo.query.order_by(Todo.date_created).all()
        # show the main page
        return render_template("index.html", tasks=tasks)

# deletion route, will be expecting a task id
@app.route('/delete/<int:id>')
def delete(id):
    # get task by id, or 404
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting that task."
    
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