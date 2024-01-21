from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app, version='1.0', title='Todo API', description='A simple Todo API')

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    status = db.Column(db.String(20), default='new')
    assigned_to = db.Column(db.String(50))

# Define namespaces
task_ns = api.namespace('tasks', description='Task operations')

@app.route('/')
def index():
    return 'Hello, this is your Flask API!'

@task_ns.route('/')
class TaskResource(Resource):
    def post(self):
        """Create a new task"""
        data = request.get_json()
        new_task = Task(title=data['title'], description=data['description'], assigned_to=data['assigned_to'])
        db.session.add(new_task)
        db.session.commit()
        return {'message': 'Task created successfully'}, 201

@task_ns.route('/<int:task_id>')
class TaskUpdateResource(Resource):
    def put(self, task_id):
        """Update task status"""
        task = Task.query.get(task_id)
        if not task:
            return {'message': 'Task not found'}, 404

        data = request.get_json()
        task.status = data['status']
        db.session.commit()
        return {'message': 'Task updated successfully'}, 200

if __name__ == '__main__':
    app.run(debug=True)
