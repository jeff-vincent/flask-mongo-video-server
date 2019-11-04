from flask import Flask, request, session, Response, jsonify
from flask_pymongo import PyMongo
from local_config import MONGO_CONNECTION_STRING
from gridfs import GridFSBucket
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = 'IsItSecret?IsItSafe?'
app.config['MONGO_URI'] = MONGO_CONNECTION_STRING
app.config['DEBUG'] = True

mongo = PyMongo(app)

@app.route('/')
def index():
    return """
        <div style="background-color: #707bb2; margin: 15px; border-radius: 5px; padding: 15px; width: 180px">
        <form action="/stream" method="post">
            <p><input type=text name=filename placeholder=" filename...">
            <p><input type=submit value="Play">
        </form>
        <form action="/get-current-users-files" method="get">
            <p><input type=submit value="Your Movie Library">
        </form>
        </div>
        <b style="margin-left:15px">Add to your movie library: </b>
        <form style="margin-left:15px" action="/upload" method="post" enctype="multipart/form-data">
            <p><input type=file name=file value="Pick a Movie">
            <p><input type=submit value="Upload">
        </form>
        <div style="background-color: #707bb2; margin: 15px; border-radius: 5px; padding: 15px; width: 180px">
        <b>Sign Up:</b>
        <form action="/signup" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value="Sign-up">
        </form>
        <b>Login:</b>
        <form action="/login" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value="Login">
        </form>
        <form action="/logout" method="get">
            <p><input type=submit value="Logout">
        </form>
        </div>


        """


@app.route('/signup', methods=['POST'])
def signup():

    try:
        username = request.form.get('username')
        password = request.form.get('password')
    
    except Exception as e:
        return 'There was a problem parsing your request. Error message: {}'.format(str(e))

    hashed_password = generate_password_hash(password)

    user = mongo.db.user.find_one({'username': username})

    if user:
        return 'Sorry, but that username is already taken. Please choose a different username.'
    
    user_id = mongo.db.user.insert({'username': username,   
                                    'password': hashed_password,
                                    'date_joined': datetime.datetime.utcnow()})

    user = mongo.db.user.find_one({'username': username})
    data = {
        'username': user['username'],
        'date_joined': user['date_joined'],
        }

    return jsonify(data)



@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
    
    except Exception as e:
        return 'There was a problem parsing your request. Error message: {}'.format(str(e))


    try:
        user = mongo.db.user.find_one({'username': username})
        if check_password_hash(user['password'],  password):
            session['username'] = username
            return 'Logged in user: {}'.format(user['username'])
        return 'Please log in.'
    except Exception as e:
        return 'Login failed: ' + (str(e))


@app.route('/logout', methods=['GET'])
def logout():
    session['username'] = ''
    return 'Logout successful.'


@app.route('/upload', methods=['POST'])
def upload():
    try:
        if session['username']:
            file = request.files['file']
            filename = file.filename
            kwargs = {
                'username': session['username']
            }
            upload = mongo.save_file(filename, file, **kwargs)
            return str(upload)
        return 'Please log in.'
    except Exception as e:
        return 'There was a problem handling your request. Error message: '.format(str(e))


@app.route('/download', methods=['POST'])
def download():
    filename = request.form['filename']
    return mongo.send_file(filename)

@app.route('/stream', methods=['POST', 'GET'])
def get_stream():
    try:
        if session['username']:
            if request.method == 'POST':
                session['filename'] = request.form['filename']
                fs = GridFSBucket(mongo.db)
                grid_out = fs.open_download_stream_by_name(session['filename'])
                contents = grid_out.read()
                return Response(contents, mimetype='video/mp4')
            else:
                fs = GridFSBucket(mongo.db)
                grid_out = fs.open_download_stream_by_name(session['filename'])
                contents = grid_out.read()
                return Response(contents, mimetype='video/mp4')

        return 'Please log in.'
    except Exception as e:
        return 'There was an error handling your request. Error message: {}'.format(str(e))

@app.route('/get-current-users-files', methods=['GET'])
def get_current_users_files():
    data = {}
    try:
        if session['username']:
            my_files = mongo.db.fs.files.find({'username': session['username']})
            for file in my_files:

                data[file['filename']] = {
                    'filename': file['filename'],
                    'username': file['username'],
                    'contentType': file['contentType'],
                    'md5': file['md5'],
                    'chunkSize': file['chunkSize'],
                    'length': file['length'],
                    'uploadDate': file['uploadDate']
                }

            return jsonify(data)
        return 'Please log in.'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)




