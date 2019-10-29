from flask import Flask, request, session, Response, stream_with_context
from flask_pymongo import PyMongo
from celery import Celery
from local_config import MONGO_CONNECTION_STRING
from gridfs import GridFSBucket

app = Flask(__name__)
app.secret_key = 'IsItSecret?IsItSafe?'
app.config['MONGO_URI'] = MONGO_CONNECTION_STRING
app.config['DEBUG'] = True

mongo = PyMongo(app)

@app.route('/')
def index():
    return """
        <b>Enter the name of the video you want to stream:</b>
        <form action="/stream" method="post">
            <p><input type=text name=filename>
            <p><input type=submit value="watch a video">
        </form>
        <b>The video's name. (Be sure to include ".mp4"):</b>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <p><input type=text name=filename>
            <p><input type=file name=file>
            <p><input type=submit value="upload file">
        </form>
        """

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = request.form['filename']
    upload = mongo.save_file(filename, file)
    return str(upload)

@app.route('/download', methods=['POST'])
def download():
    filename = request.form['filename']
    return mongo.send_file(filename)

@app.route('/stream', methods=['POST', 'GET'])
def get_stream():
    if request.method == 'POST':
        session['filename'] = request.form['filename']
        db = mongo.cx.get_database('test')
        fs = GridFSBucket(db)
        grid_out = fs.open_download_stream_by_name(session['filename'])
        contents = grid_out.read()
        return Response(contents, mimetype='video/mp4')
    else:
        db = mongo.cx.get_database('test')
        fs = GridFSBucket(db)
        grid_out = fs.open_download_stream_by_name(session['filename'])
        contents = grid_out.read()
        return Response(contents, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)




