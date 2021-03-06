from flask import Flask, request, url_for, session
import flask
from flask.helpers import flash
from flask.templating import render_template
from werkzeug.utils import redirect, secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os, re
import sys

from controllers import userController, dogController

# Import dataHandler
from handlers.userDataHandler import dataHandler
# Import imageHandler
from handlers.imageHandler import imageHandler

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
    if session.get('loggedin') != True:
        return render_template("index.html")
    else: 
        return redirect("dashboard")

# USER #

@app.route("/login", methods=["POST", "GET"])
def login():
    return userController.user.login()

@app.route("/logout")
def logout():
    return userController.user.logout()

@app.route("/register", methods=["POST", "GET"])
def register():
    return userController.user.register()

@app.route("/dashboard")
def dashboard():
    if session.get('loggedin') == True: 
        return render_template("dashboard.html")
    else:
        return redirect("/login")

@app.route("/user/profile")
def profile():
    return userController.user.profile()

@app.route("/user/profile/edit", methods=["POST", "GET"])
def editUserProfile():
    return userController.user.editUserProfile()

###

# DOG #

@app.route("/dog/add", methods=["POST", "GET"])
def addDog():
    return dogController.dog.addDog()

@app.route("/dog/<name>")
def dogProfile(name = None):
    return dogController.dog.dogProfile(name)

@app.route("/dog/<name>/edit", methods=["POST", "GET"])
def editDogProfile(name = None):
    return dogController.dog.editDogProfile(name)

###

if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = sys.argv[1].split(":")
        host = args[0]
        port = int(args[1])
    else:
        host = "0.0.0.0"
        port = 6060
    app.run(debug=True, host=host, port=port)