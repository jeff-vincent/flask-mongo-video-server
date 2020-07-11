from flask import Flask, request, session
from local_config import MONGO_CONNECTION_STRING
from gridfs import GridFSBucket
from flask_pymongo import PyMongo
from celery import Celery

from index import index_view
from user_management import UserManagement
from video_management import VideoManagement

app = Flask(__name__)
app.secret_key = 'IsItSecret?IsItSafe?'
app.config['MONGO_URI'] = MONGO_CONNECTION_STRING
app.config['DEBUG'] = True
app.config['CELERY_BROKER_URL'] = 'amqp://jdv:jdv@localhost:5672/v_host'

mongo = PyMongo(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
long_task = Celery(app.name, broker='amqp://guest:guest@localhost:5672/v_host')

@celery.task
@app.route('/')
def index():
    return index_view

@celery.task
@app.route('/signup', methods=['POST'])
def signup():
    user_management = UserManagement(request, mongo)
    result = user_management.signup()
    return result

@celery.task
@app.route('/login', methods=['POST'])
def login():
    user_management = UserManagement(request, mongo)
    result = user_management.login()
    return result

@celery.task
@app.route('/logout', methods=['GET'])
def logout():
    session['username'] = ''
    return 'Logout successful.'

@celery.task
@app.route('/get-current-users-files', methods=['GET'])
def get_current_users_files():
    user_management = UserManagement(request, mongo)
    result = user_management.get_users_files()
    return result

@celery.task
@app.route('/get-public-files', methods=['GET'])
def get_public_files():
    video_management = VideoManagement(request, mongo)
    result = video_management.get_public_files()
    return result

@long_task.task
@app.route('/upload', methods=['POST'])
def upload():
    video_management = VideoManagement(request, mongo)
    result = video_management.upload()
    return result

@long_task.task
@app.route('/download', methods=['POST'])
def download():
    filename = request.form['filename']
    return mongo.send_file(filename)

@long_task.task
@app.route('/stream', methods=['POST', 'GET'])
def get_stream():
    video_management = VideoManagement(request, mongo)
    result = video_management.get_stream()
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




