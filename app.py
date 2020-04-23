from flask import Flask, render_template, request, redirect
#import json

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1234@localhost/todolist"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Task(db.Model) :
    __tablename__ = 'Tasks'
    id = db.Column(db.Integer, primary_key = True )
    content = db.Column(db.String(100), nullable = False)
    creationDate = db.Column(db.DateTime)

    def __repr__(self) :
        return f'<Task {self.content}>'





#tasks = [
    #  { "id" : 1, "name" : 'Watch TV'},
    #  { "id" : 2, "name" : 'buy eggs'}
   
#]

# try :
#     tasksFile = open('./tasks.json', 'r')
#     tasks = json.load(tasksFile)
#     tasksFile.close()
# except :
#     tasks = []

# def writeTasks() :
#     tasksFile = open('./tasks.json', 'w')
#     json.dump(tasks, tasksFile, indent = 4)
#     tasksFile.close()

@app.route('/')
def index() :

    tasks = Task.query.all()
    #print(tasks)
    return render_template('index.html', tasks = tasks)

@app.route('/add-task', methods = [ 'POST' ])
def addTask() :
    taskName = request.form.get('new-task')

    task = Task(content = taskName, creationDate = datetime.now())

    db.session.add(task)
    db.session.commit()

    # m = 0
    # for task in tasks :
    #     if task.get('id') > m :
    #         m = task.get('id')

    # task = {
    #     'id' : m + 1,
    #     "name" : taskName
        
    # }
    # tasks.append(task)
    
    # writeTasks()
    return redirect('/')

@app.route('/remove-task', methods = [ 'GET' ])
def removeTask() :
    taskId = int(request.args.get('id'))

    task = Task.query.filter_by(id = taskId).first()
    #print(task)
    db.session.delete(task)
    db.session.commit()

    # for task in tasks :
    #     print(task)
    #     if task.get('id') == taskId :
    #         tasks.remove(task)
    
    # writeTasks()
    return redirect('/')

@app.route('/edit-task', methods = [ 'GET' ])
def editTask() :
    taskId = int(request.args.get('id'))
    name = ''

    task = Task.query.filter_by(id = taskId).first()
    name = task.content
    # for task in tasks :
    #     if task.get('id') == taskId :
    #         name = task.get('name')

    return render_template('item-edit.html', taskValue = name, id = taskId)

@app.route('/save-task', methods = [ 'POST' ])
def saveTask() :
    taskName = request.form.get('edit-task')
    taskId = int(request.form.get('id'))
   
    task = Task.query.filter_by(id = taskId).first()
    # print(task)
    task.content = taskName
    db.session.commit()
    # for task in tasks :
    #    if task.get('id') == taskId :
    #        task['name'] = taskName

    # writeTasks()
    return redirect('/')

if __name__ == '__main__' :
    app.run(debug=True)

