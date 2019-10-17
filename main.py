from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route('/')
def index():
    return "Media Server is up."

@app.route('/upload', methods=['POST'])
def upload():
    filename = request.form['filename']
    return PyMongo.save_file(filename)

@app.route('/download', methods=['POST'])
def download():
    filename = request.form['filename']
    return PyMongo.send_file(filename)

if __name__ == '__main__':
    app.run()

