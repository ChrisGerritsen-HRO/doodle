from flask import Flask, request,url_for
import flask
from flask.helpers import flash
from flask.templating import render_template
from werkzeug.utils import redirect, secure_filename
import sqlite3
import os

app = Flask(__name__)

SECRET_KEY = os.urandom(24)
DATABASE = 'doodle.db'
UPLOADFOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# app = flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOADFOLDER

def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def main():
    return "<p>Index page!</p>"

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect("/")
        # file = request.file['file']

        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect("/")
        # if file and allow_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config[UPLOADFOLDER], filename))

        try:
            nm = request.form['name']
            email = request.form['email']
            birthday = request.form['birthday']
            profilePic = request.form['profilepic']
            passwrd = request.form['password']
            confirmPasswrd = request.form['confirmpass']

            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user (name, email, birthday, profilepic, password) VALUES (?,?,?,?,?)", (nm, email, birthday, profilePic, passwrd))
                
                con.commit()
        except:
            pass
        finally:
            con.close()
            return redirect("/")

    return render_template("register.html")
