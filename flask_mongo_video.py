from flask import Flask, request, session, Response, jsonify, render_template
from local_config import MONGO_CONNECTION_STRING
from gridfs import GridFSBucket
from flask_pymongo import PyMongo

from index import index_view
from user_management import UserManagement
from video_management import VideoManagement

app = Flask(__name__)
app.secret_key = 'IsItSecret?IsItSafe?'
app.config['MONGO_URI'] = MONGO_CONNECTION_STRING
app.config['DEBUG'] = True

mongo = PyMongo(app)

@app.route('/')
def index():

        return index_view


@app.route('/signup', methods=['POST'])
def signup():
    user_management = UserManagement(request, mongo)
    result = user_management.signup()
    
    return result


@app.route('/login', methods=['POST'])
def login():
    user_management = UserManagement(request, mongo)
    result = user_management.login()
    
    return result


@app.route('/logout', methods=['GET'])
def logout():
    session['username'] = ''
    
    return 'Logout successful.'


@app.route('/get-current-users-files', methods=['GET'])
def get_current_users_files():
    user_management = UserManagement(request, mongo)
    result = user_management.get_users_files()
    
    return result


@app.route('/get-public-files', methods=['GET'])
def get_public_files():
    video_management = VideoManagement(request, mongo)
    result = video_management.get_public_files()

    return result


@app.route('/upload', methods=['POST'])
def upload():
    video_management = VideoManagement(request, mongo)
    result = video_management.upload()

    return result


@app.route('/download', methods=['POST'])
def download():
    filename = request.form['filename']
    return mongo.send_file(filename)


@app.route('/stream', methods=['POST', 'GET'])
def get_stream():
    video_management = VideoManagement(request, mongo)
    result = video_management.get_stream()

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)




