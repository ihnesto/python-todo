from flask import Flask, render_template, request, redirect
from flask_mongoengine import MongoEngine
import mongoengine as me
from datetime import datetime

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "todolist",
}
db = MongoEngine(app)

class Task(me.Document):
    content = me.StringField(required=True)
    creationDate = me.DateTimeField()
    expiredDate = me.DateTimeField(required=True)
    
    def __repr__(self) :
        return f'<Task {self.content}>'

@app.route('/')
def index() :
    order = request.args.get('sort')
    if order is not None :
        if order == 'asc' :
            tasks = Task.objects.order_by('expiredDate').all()
        elif order == 'desc' :
            tasks = Task.objects.order_by('-expiredDate').all()
        else :
            tasks = Task.objects.all()
    else :
        tasks = Task.objects.all()

    modTasks = []
    for task in tasks :
        fTime = task.expiredDate
        nTime = datetime.now()
        diff = (fTime - nTime).total_seconds()
        if diff > 0 :
            marked = False
        else :
            marked = True
        modTasks.append({
            "task": task,
            "marked": marked
        })

    return render_template('index.html', tasks = modTasks)

@app.route('/add-task', methods = [ 'POST' ])
def addTask() :
    taskName = request.form.get('new-task')
    expDate = request.form.get('exp-date')
    expTime = request.form.get('exp-time')
    print(expDate, expTime)

    fullDateTime = f'{expDate} {expTime}:00'
    #print(fullDateTime)
    task = Task(content = taskName, creationDate = datetime.now(), expiredDate = fullDateTime)
    task.save()
    
    return redirect('/')

@app.route('/remove-task', methods = [ 'GET' ])
def removeTask() :
    taskId = request.args.get('id')

    task = Task.objects(pk=taskId).first()
    task.delete()

    return redirect('/')

@app.route('/edit-task', methods = [ 'GET' ])
def editTask() :
    taskId = request.args.get('id')
    name = ''

    task = Task.objects(pk=taskId).first()
    name = {
        'content' : task.content,
        'expiredDate' : datetime.date(task.expiredDate),
        'expiredTime' : datetime.time(task.expiredDate)

    } 
    return render_template('item-edit.html', task = name, id = taskId)

@app.route('/save-task', methods = [ 'POST' ])
def saveTask() :
    taskName = request.form.get('edit-task')
    
    taskId = request.form.get('id')
    expDate = request.form.get('exp-date')
    expTime = request.form.get('exp-time')
    task = Task.objects(pk=taskId).first()
    # print(Task)
    task.content = taskName
    task.expiredDate =  fullDateTime = f'{expDate} {expTime}'
    task.save()
    
    return redirect('/')

if __name__ == '__main__' :
    app.run(debug=True)

