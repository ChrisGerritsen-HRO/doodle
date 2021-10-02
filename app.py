from flask import Flask, request,url_for
import flask
from flask.templating import render_template
from werkzeug.utils import redirect
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'doodle.db'
UPLOADFOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOADFOLDER

def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def main():
    return "<p>Index page!</p>"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            nm = request.form['name']
            email = request.form['email']
            birthday = request.form['birthday']
            profilePic = request.form['profilepic']
            passwrd = request.form['password']
            confirmPasswrd = request.form['confirmpass']

            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user (name, email, birthday, profilepic, password, confirmpass) VALUES (?,?,?,?,?,?)", (nm, email, birthday, profilePic, passwrd, confirmPasswrd))
                
                con.commit()
        except:
            pass
        finally:
            con.close()
            return redirect(url_for(main))

    return render_template("register.html")
