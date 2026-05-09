from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests

BACKEND_URL = 'http://127.0.0.1:9000'

app = Flask(__name__)

@app.route('/')
def home(error=None):
    day_of_week = datetime.today().strftime('%A')
    current_time = datetime.now().strftime('%H:%M:%S')
    return render_template('index.html', day_of_week=day_of_week, current_time=current_time, error=error)

@app.route('/todo')
def todo():    
    return render_template('todo.html')

@app.route('/submit', methods=['POST'])
def submit():
    error = None
    data = dict(request.form)
    if data["name"] == "" or data["password"] == "":
        error = "All fields must be entered"
    else:
        response = requests.post(BACKEND_URL + '/submit', json=data)
        if response.status_code == 500 or response.status_code == 400 or response.status_code == 401:
           error = "Error Occurred! Please try after some time"
        else:
            return 'Data Submitted Successfully!'
    return home(error)
      
@app.route('/get_data')
def get_data():
    try:
        response = requests.get(BACKEND_URL + '/view')
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return 'error'

@app.route('/submittodoitem', methods=['POST'])
def submittodoitem():
    error = None
    data = dict(request.form)
    if data["name"] == "" or data["description"] == "":
        error = "All fields must be entered"
    else:
        response = requests.post(BACKEND_URL + '/submittodoitem', json=data)
        if response.status_code == 500 or response.status_code == 400 or response.status_code == 401:
           error = "Error Occurred! Please try after some time"
        else:
            return 'Todo Item Added Successfully!'
    return home(error)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000,debug=True)