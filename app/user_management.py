import datetime
from flask import jsonify
from flask import session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash



class UserManagement:
    def __init__(self, request, mongo):
        self.request = request
        self.mongo = mongo

    def signup(self):
        try:
            username = self.request.form.get('username')
            password = self.request.form.get('password')
        except Exception as e:
            return 'There was a problem parsing your request.\
             Error message: {}'.format(str(e))
        hashed_password = generate_password_hash(password)
        user = self.mongo.db.user.find_one({'username': username})
        if user:
            return 'Sorry, but that username is already taken.\
            Please choose a different username.'
        self.mongo.db.user.insert({'username': username,   
                                        'password': hashed_password,
                                        'date_joined': datetime.datetime.utcnow()})
        user = self.mongo.db.user.find_one({'username': username})
        data = {
            'username': user['username'],
            'date_joined': user['date_joined'],
            }

        return jsonify(data)

    def login(self):
        try:
            username = self.request.form.get('username')
            password = self.request.form.get('password')
        except Exception as e:
            return 'There was a problem parsing your request.\
             Error message: {}'.format(str(e))
        try:
            user = self.mongo.db.user.find_one({'username': username})
            if check_password_hash(user['password'],  password):
                session['username'] = username

                return 'Logged in user: {}'.format(user['username'])
            return 'Please log in.'
        except Exception as e:

            return 'Login failed: {}'.format(str(e))

    def get_users_files(self):
        data = {}
        try:
            if session['username']:
                my_files = self.mongo.db.fs.files.find({'username': session['username']})
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
            return 'There was a problem handling your request.\
            Error message: {}'.format(str(e))
