from flask import Flask, request
from flask_pymongo import PyMongo
from local_config import MONGO_CONNECTION_STRING

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_CONNECTION_STRING
app.config['DEBUG'] = True
mongo = PyMongo(app)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

