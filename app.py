from flask import Flask, session
import flask
from flask.helpers import flash
from flask.templating import render_template
from werkzeug.utils import redirect
import os

# Import userController
from controllers import userController

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
        return "<p>Index page!</p>"
    else: 
        return redirect("/dashboard")

@app.route("/login", methods=["POST", "GET"])
def login():
    userController.user.login()

@app.route("/logout")
def logout():
    userController.user.logout()

@app.route("/register", methods=["POST", "GET"])
def register():
    userController.user.register()

@app.route("/dashboard")
def dashboard():
    if session.get('loggedin') == True: 
        return render_template("dashboard.html")
    else:
        return redirect("/")