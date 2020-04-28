import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='todolist',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()       
sql = "SELECT * FROM TASKS"
cursor.execute(sql, ())
connection.commit()
tasks = cursor.fetchall()
for task in tasks :
    print(task.get('content'))

connection.close()


with len(tasks) as cursor:

cursor = connection.cursor()    