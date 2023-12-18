"""
Flask App with SQLite for Task Management

This simple Flask app allows users to manage tasks. Tasks are stored in an SQLite database.
Users can view a list of tasks, mark tasks as completed, and add new tasks.

Author: Shashikumar KL
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# pylint: disable=too-few-public-methods
class Task(db.Model):
    """
    Task Model

    Represents a task with a unique identifier, a taskname, and a completion status.
    """
    id = Column(Integer, primary_key=True)
    taskname = Column(String(200), nullable=False)
    completed = Column(Boolean, default=False)

    def __repr__(self):
        """
        String representation of the Task object.

        Returns:
            str: A string representation of the Task object.
        """
        return f"Task(id={self.id}, description={self.taskname}, completed={self.completed})"

@app.route('/')
def home():
    """
    Home Route

    Displays a list of tasks on the homepage.

    Returns:
        str: Rendered HTML template showing the list of tasks.
    """
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    """
    Add Task Route

    Adds a new task to the database based on user input.

    Returns:
        str: Redirects to the homepage after adding the task.
    """
    taskname = request.form['taskname']
    new_task = Task(taskname=taskname)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/toggle_task/<int:task_id>')
def toggle_task(task_id):
    """
    Toggle Task Route

    Toggles the completion status of a task.

    Args:
        task_id (int): The unique identifier of the task.

    Returns:
        str: Redirects to the homepage after toggling the task's completion status.
    """
    task = Task.query.get(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
