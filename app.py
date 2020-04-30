from flask import Flask, render_template, request, redirect
import pymysql.cursors

from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index() :

    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='todolist',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()

    order = request.args.get('sort')
    if order is not None :
        if order == 'asc' :
            sql = "select * from tasks order by expiredDate"
        elif order == 'desc' :
            sql = "select * from tasks order by expiredDate desc"
        else :
            sql = "select * from tasks"
    else :
        sql = "select * from tasks"
    cursor.execute(sql, ())
    tasks = cursor.fetchall()
    print(tasks)
    modTasks = []
    for task in tasks :
        fTime = task.get('expiredDate')
        nTime = datetime.now()
        if nTime > fTime :
            marked = False
        else :
            marked = True
        modTasks.append({
            "task": task,
            "marked": marked
        })
    connection.close()
    return render_template('index.html', tasks = modTasks)

@app.route('/add-task', methods = [ 'POST' ])
def addTask() :
    taskName = request.form.get('new-task')
    expDate = request.form.get('exp-date')
    expTime = request.form.get('exp-time')
    print(expDate, expTime)

    fullDateTime = f'{expDate} {expTime}:00'
    #print(fullDateTime)
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='todolist',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    sql = "insert into tasks(content, creationDate, expiredDate) values(%s, %s, %s)"
    cursor.execute(sql, (taskName, str(datetime.now()), fullDateTime))
    connection.commit()
    connection.close()
    return redirect('/')

@app.route('/remove-task', methods = [ 'GET' ])
def removeTask() :
    taskId = int(request.args.get('id'))
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='todolist',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    sql = "delete from tasks where id=%s"
    cursor.execute(sql, (taskId))
    connection.commit()
    connection.close()
    return redirect('/')

@app.route('/edit-task', methods = [ 'GET' ])
def editTask() :
    taskId = int(request.args.get('id'))
    
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='todolist',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    sql = "select * from tasks where id=%s"
    cursor.execute(sql, (taskId))
    task = cursor.fetchall()
    print(task)
    
    name = {
        'content' : task[0].get('content'),
        'expiredDate' : datetime.date(task[0].get('expiredDate')),
        'expiredTime' : datetime.time(task[0].get('expiredDate'))

    } 
    connection.close()
    return render_template('item-edit.html', task = name, id = taskId)

@app.route('/save-task', methods = [ 'POST' ])
def saveTask() :
    taskName = request.form.get('edit-task')
    
    taskId = int(request.form.get('id'))
    expDate = request.form.get('exp-date')
    expTime = request.form.get('exp-time')
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='todolist',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    sql = "update tasks set content=%s, expiredDate=%s where id=%s"
    cursor.execute(sql, (taskName, f'{expDate} {expTime}', taskId))
    connection.commit()
    connection.close()
    return redirect('/')

if __name__ == '__main__' :
    app.run(debug=True)

