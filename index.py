from flask import Flask, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
import os
import requests

from werkzeug.utils import secure_filename

token = "e6844e3e47c04efdae0a0d32b7cb36ca"
filename = "/harvard.wav"
app = Flask(__name__)
app.secret_key = "secret key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/products"
mongo = PyMongo(app)

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXT = {'mp3','wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


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
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
        id = mongo.db.user.insert({
            'name': _name,
            'email': _email,
            'matricNo': _matricNo
        })
        response = jsonify('User created')
        response.status_code = 200
        return response
    else:
        return not_found()


@app.route('/all')
def students():
    students = mongo.db.user.find()
    resp = dumps(students)
    return resp


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
    app.run(port=5000)
