from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from pymongo import MongoClient, errors

load_dotenv()

MONGO_URI=os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.test
collection = db['flask-tutorial']

app = Flask(__name__)

@app.route('/api')
def get_list():
    file = open("user-list.json", "r")
    content = file.read()
    file.close()

    return content

@app.route('/submit', methods=['POST'])
def submit():
    form_data = dict(request.json)
    try:
        result = collection.insert_one(form_data)
        if result.acknowledged:
            return 'Data Submitted Successfully!'
        
    except errors.PyMongoError:
        raise Exception("Something went wrong!")
    except errors.OperationFailure:
        raise Exception("Something went wrong!")

@app.route('/view')
def view():
    try:
        data = collection.find()
        data = list(data)
        for item in data:
            del item['_id']

        data = { 
            'data' : data 
        }
        
        return data
    except errors.OperationFailure:
        return 'error'

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=9000,debug=True)
