from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://jeff:AsspWord@cluster0-intvw.mongodb.net/test?retryWrites=true&w=majority'
app.config['DEBUG'] = True
mongo = PyMongo(app)

@app.route('/')
def index():
    return """
    <form action="/upload" method="post" enctype="multipart/form-data">
        <p><input type=text name=filename>
        <p><input type=file name=file>
        <p><input type=submit value="upload file">
    </form>
    """

@app.route('/upload', methods=['POST'])
def upload():
    filename = request.form['filename']
    file = request.files['file']
    return mongo.save_file(filename, file)

@app.route('/download', methods=['POST'])
def download():
    filename = request.form['filename']
    return mongo.send_file(filename)

if __name__ == '__main__':
    app.run()

