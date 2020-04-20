from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tasks = [
    { "id" : 1, "name" : 'Watch TV'},
    { "id" : 2, "name" : 'buy eggs'}
   
]

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
    return redirect('/')

@app.route('/remove-task', methods = [ 'GET' ])
def removeTask() :
    taskId = int(request.args.get('id'))

    for task in tasks :
        print(task)
        if task.get('id') == taskId :
            tasks.remove(task)

    return redirect('/')

if __name__ == '__main__' :
    app.run(debug=True)

