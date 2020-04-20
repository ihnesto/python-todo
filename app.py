from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

#tasks = [
    #  { "id" : 1, "name" : 'Watch TV'},
    #  { "id" : 2, "name" : 'buy eggs'}
   
#]

try :
    tasksFile = open('./tasks.json', 'r')
    tasks = json.load(tasksFile)
    tasksFile.close()
except :
    tasks = []

def writeTasks() :
    tasksFile = open('./tasks.json', 'w')
    json.dump(tasks, tasksFile, indent = 4)
    tasksFile.close()

@app.route('/')
def index() :
    return render_template('index.html', tasks = tasks)

@app.route('/add-task', methods = [ 'POST' ])
def addTask() :
    taskName = request.form.get('new-task')

    m = 0
    for task in tasks :
        if task.get('id') > m :
            m = task.get('id')

    task = {
        'id' : m + 1,
        "name" : taskName
        
    }
    tasks.append(task)
    
    writeTasks()
    return redirect('/')

@app.route('/remove-task', methods = [ 'GET' ])
def removeTask() :
    taskId = int(request.args.get('id'))

    for task in tasks :
        print(task)
        if task.get('id') == taskId :
            tasks.remove(task)
    
    writeTasks()
    return redirect('/')

@app.route('/edit-task', methods = [ 'GET' ])
def editTask() :
    taskId = int(request.args.get('id'))
    name = ''
    for task in tasks :
        if task.get('id') == taskId :
            name = task.get('name')

    return render_template('item-edit.html', taskValue = name, id = taskId)

@app.route('/save-task', methods = [ 'POST' ])
def saveTask() :
    taskName = request.form.get('edit-task')
    taskId = int(request.form.get('id'))
   
    for task in tasks :
       if task.get('id') == taskId :
           task['name'] = taskName

    writeTasks()
    return redirect('/')

if __name__ == '__main__' :
    app.run(debug=True)

