from flask import Flask, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
import os
import re
import requests
import json
from werkzeug.utils import secure_filename

password = "o96aBKVPPLbUCTAn";
DBUSER = "voice_adminBaDm1n"
PASSWORD = "BaDm1n"
URL = "mongodb://" + DBUSER + ":" + PASSWORD + "@ds361998.mlab.com:61998/voice_attendance?retryWrites=false"

token = "e6844e3e47c04efdae0a0d32b7cb36ca"
app = Flask(__name__)
app.secret_key = "secret key"
app.config["MONGO_URI"] = URL
mongo = PyMongo(app)

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXT = {'mp3', 'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filed):
    return '.' in filed and filed.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@app.route('/upload', methods=['POST'])
def upload():
    message = {
        'status': 200,
        'data': []
    }
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify('Not in file')
    file = request.files['file']
    if file.filename == '':
        return jsonify('No file')
    if file and allowed_file(file.filename):
        filenamed = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filenamed))
        return jsonify('Success')
    else:
        return jsonify('Not successful')


@app.route('/register', methods=['POST'])
def register():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _matricNo = _json['matricNo']



    if _name and _email and _matricNo and request.method == 'POST':
        validate = mongo.db.user.find_one({
            "matricNo": _matricNo
        })
        exist = []
        validate.pop('_id')
        exist.append(validate)
        if len(exist) >= 1 :
            message  = {
                "message" : "Student exist",
                # "student":exist,
                "status": False
            }
            jsed = jsonify(message)
            jsed.status_code = 422
            return jsed
        else:
            id = mongo.db.user.insert({
                'name': _name,
                'email': _email,
                'matricNo': _matricNo
            })
            message = {
                "status": True,
                "message": "Student Created"
            }
            response = jsonify(message)

            response.status_code = 201
            return response

    else:
        return not_found()


@app.route('/student', methods=['POST'])
def verify():
    _json = request.json
    _digit = _json['digit']
    student = []
    try:
        response = mongo.db.user.find_one({
            "matricNo": {
                "$regex": _digit + "$"
                # "$regex" : ".*"+_digit+ "*"
            }
        })
        response.pop('_id')
        student.append(response)
        if len(student) >= 1:
            # student.status_code = 200
            message = {
                "status": True,
                "message": response
            }
            sent = jsonify(message)
            sent.status_code = 200
            return sent
        else:
            message = {
                "Status": False,
                "message": "User doesnt exist"
            }
            notfound = jsonify(message)
            not_found.status_code = 422
            return notfound
    except:
        message = {
            "message" : "Not valid",
            "status":False
        }
        return message






@app.route('/all')
def students():
    allStudents = mongo.db.user.find()
    resp = dumps(allStudents)
    message = {
        "status": True,
        "students": resp
    }
    send = jsonify(message)
    send.status_code = 200
    return send


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run(port=5001)
