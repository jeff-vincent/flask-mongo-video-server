from flask import Flask, request, session
from flask_pymongo import PyMongo
from celery import Celery
from local_config import MONGO_CONNECTION_STRING

app = Flask(__name__)
app.secret_key = 'IsItSecret?IsItSafe?'
app.config['MONGO_URI'] = MONGO_CONNECTION_STRING
app.config['DEBUG'] = True
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

mongo = PyMongo(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/')
def index():
    return "Server is up."

@app.route('/upload', methods=['POST'])
def upload():
    filename = request.form['filename']
    file = request.files['file']
    upload = mongo.save_file(filename, file)
    return str(upload)

@app.route('/download', methods=['POST'])
def download():
    filename = request.form['filename']
    return mongo.send_file(filename)

@app.route('/stream', methods=['GET', 'POST'])
def stream():
    if request.method == 'POST':
        filename = request.form['filename']
        session['filename'] = filename
    else:
        filename = session['filename']
    chunk = mongo.db.fs.chunks.find_one()
    print(chunk)
    return str(chunk)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

