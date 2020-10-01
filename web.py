import flask
import pymongo
import json
import datetime
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True
client = pymongo.MongoClient('127.0.0.1', 27017)


@app.route('/get_users', methods=['GET'])
def get_users():
    db = client['testdb']
    results = db['login_users'].find()
    response = []
    for document in results:
        document['_id'] = str(document['_id'])
        response.append(document)
    print(response, flush=True)    
    return json.dumps(response)

@app.route('/create_user', methods=['POST'])
def create_users():
    print('running post')
    req_data = request.get_json()
    user = {
        "user_id" : req_data['user_id'],
        "name" : req_data['name'],
        "password" : req_data['password'],
        "status": req_data['status'],
        "created_date" : datetime.datetime.utcnow()
    }
    db = client['testdb']
    result = db['login_users'].insert_one(user)
    print(result.inserted_id, flush=True)
    # return json.dumps(user)
    return ('Created document id: ' + str(result.inserted_id))

app.run()