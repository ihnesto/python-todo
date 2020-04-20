from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tasks = [
    { "id" : 1, "name" : 'Watch TV'},
    { "id" : 2, "name" : 'buy eggs'}
   
]

@app.route('/')
def index() :
    return render_template('index.html', tasks = tasks)

if __name__ == '__main__' :
    app.run(debug=True)

