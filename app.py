from flask import Flask, request,url_for
import flask
from flask.helpers import flash
from flask.templating import render_template
from werkzeug.utils import redirect, secure_filename
from werkzeug.security import generate_password_hash
import sqlite3
import os, re

from handlers.dataHandler import dataHandler
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
    return "<p>Index page!</p>"

@app.route("/login", methos=["GET", "POST"])
def login():
    pass

@app.route("/register", methods=["POST", "GET"])
def register():
    msg = ''
    if request.method == "POST" and request.form['password'] == request.form['confirmpass']:
        sqlConnection = sqlite3.connect(DATABASE)
        cursor = sqlConnection.cursor()
        userSelect = """SELECT * FROM user WHERE email = ?"""
        cursor.execute(userSelect, (request.form['email'], ))
        user = cursor.fetchone()

        if user:
            print("Account bestaat al!")
            msg = 'Account bestaat al!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', request.form['email']):
            msg = 'Geen geldig email adres!'
        else:
            file = request.files['profilepic']
            fileName = secure_filename(file.filename)
            imageHandler.userImageHandler(file, fileName)

            hashPasswrd = generate_password_hash(request.form['password'], "sha256")

            userData = (
                request.form['name'],
                request.form['email'],
                request.form['birthday'],
                fileName,
                hashPasswrd,
            )
                
            dataHandler.insertUserData(userData)

            return redirect("/")

    return render_template("register.html", msg = msg)