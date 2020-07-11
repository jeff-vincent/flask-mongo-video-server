from flask import session, Response, jsonify
from gridfs import GridFSBucket

class VideoManagement:
    def __init__(self, request, mongo):
        self.request = request
        self.mongo = mongo


    def upload(self):
        try:
            if session['username']:
                file = self.request.files['file']
                if self.request.form.get('public'):
                    public = True
                else:
                    public = False
                filename = file.filename
                kwargs = {
                    'username': session['username'],
                    'public': public
                }
                upload = self.mongo.save_file(filename, file, **kwargs)
                return str(upload)
            return 'Please log in.'
        except Exception as e:
            return 'There was a problem handling your request.\
            Error message: '.format(str(e))


    def get_public_files(self):
        data = {}
        try:
            if session['username']:
                public_files = self.mongo.db.fs.files.find({'public': True})
                for file in public_files:

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
            return 'Please log in.'


    def get_stream(self):
        try:
            if session['username']:
                if self.request.method == 'POST':
                    session['filename'] = self.request.form['filename']
                    fs = GridFSBucket(self.mongo.db)
                    grid_out = fs.open_download_stream_by_name(session['filename'])
                    contents = grid_out.read()
                    return Response(contents, mimetype='video/mp4')
                else:
                    fs = GridFSBucket(self.mongo.db)
                    grid_out = fs.open_download_stream_by_name(session['filename'])
                    contents = grid_out.read()
                    return Response(contents, mimetype='video/mp4')

            return 'Please log in.'
        except Exception as e:
            return 'There was an error handling your request.\
            Error message: {}'.format(str(e))