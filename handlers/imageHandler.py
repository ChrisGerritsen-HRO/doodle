import os
from flask import Flask

SECRET_KEY = os.urandom(24)
USER_UPLOADFOLDER = 'images/user'
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['USER_UPLOAD_FOLDER'] = USER_UPLOADFOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

class imageHandler():

    def userImageHandler(file, fileName):
        if fileName != '':
            file_ext = os.path.splitext(fileName)[1]
        if file_ext not in app.config['ALLOWED_EXTENSIONS']:
            os.abort(400)
        file.save(os.path.join(app.config['USER_UPLOAD_FOLDER'], fileName))