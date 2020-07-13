from flask import Flask, request, session
from local_config import MONGO_CONNECTION_STRING, SECRET_KEY
from gridfs import GridFSBucket
from flask_pymongo import PyMongo
from celery import Celery

from index import index_view
from user_management import UserManagement
from video_management import VideoManagement

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['MONGO_URI'] = MONGO_CONNECTION_STRING
app.config['DEBUG'] = True

mongo = PyMongo(app)

celery_one = Celery(app.name, 
queue='short_tasks', 
broker='amqp://guest:guest@172.17.0.2:5672', 
backend=MONGO_CONNECTION_STRING)

celery_two = Celery(app.name, 
queue='long_tasks', 
broker='amqp://guest:guest@172.17.0.2:5672', 
backend=MONGO_CONNECTION_STRING)


@app.route('/')
def index():
    task = _index.apply_async(queue='short_tasks')
    return task.get()

@celery_one.task
def _index():
    return index_view

@celery_one.task
@app.route('/signup', methods=['POST'])
def signup():
    user_management = UserManagement(request, mongo)
    result = user_management.signup()
    return result

@celery_one.task
@app.route('/login', methods=['POST'])
def login():
    user_management = UserManagement(request, mongo)
    result = user_management.login()
    return result

@celery_one.task
@app.route('/logout', methods=['GET'])
def logout():
    session['username'] = ''
    return 'Logout successful.'

@celery_one.task
@app.route('/get-current-users-files', methods=['GET'])
def get_current_users_files():
    user_management = UserManagement(request, mongo)
    result = user_management.get_users_files()
    return result

@celery_one.task
@app.route('/get-public-files', methods=['GET'])
def get_public_files():
    video_management = VideoManagement(request, mongo)
    result = video_management.get_public_files()
    return result

@celery_two.task
@app.route('/upload', methods=['POST'])
def upload():
    video_management = VideoManagement(request, mongo)
    result = video_management.upload()
    return result

@celery_two.task
@app.route('/download', methods=['POST'])
def download():
    filename = request.form['filename']
    return mongo.send_file(filename)


@app.route('/stream', methods=['POST', 'GET'])
def get_stream():
    task = _get_stream.apply_async(queue='long_tasks')
    return task.get()

@celery_two.task
def _get_stream():
    video_management = VideoManagement(request, mongo)
    result = video_management.get_stream()
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)




