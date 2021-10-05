from flask import Flask, request,url_for
import flask
from flask.helpers import flash
from flask.templating import render_template
from werkzeug.utils import redirect, secure_filename
import sqlite3
import os

SECRET_KEY = os.urandom(24)
DATABASE = 'doodle.db'
UPLOADFOLDER = 'images'
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOADFOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

@app.route("/")
def main():
    return "<p>Index page!</p>"

@app.route("/register", methods=["POST", "GET"])
def register():
    # Iets nieuws zoeken voor data opslaan in database en functie netter maken.
    if request.method == "POST" and request.form['password'] == request.form['confirmpass']:
        file = request.files['profilepic']
        fileName = secure_filename(file.filename)
        if fileName != '':
            file_ext = os.path.splitext(fileName)[1]
        if file_ext not in app.config['ALLOWED_EXTENSIONS']:
            os.abort(400)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))

        try:
            nm = request.form['name']
            email = request.form['email']
            birthday = request.form['birthday']
            profilePic = request.form['profilepic']
            passwrd = request.form['password']

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