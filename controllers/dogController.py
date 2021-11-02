from flask import Flask, request, url_for, session
import flask
from flask.helpers import flash
from flask.templating import render_template
from werkzeug.utils import redirect, secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os, re

# Import dataHandler
from handlers.dogDataHandler import dataHandler
# Import imageHandler
from handlers.imageHandler import imageHandler

SECRET_KEY = os.urandom(24)
DATABASE = 'doodle.db'
UPLOADFOLDER = 'static/dog'
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

class dog():
    
    def addDog():
        if request.method == "POST":
            file = request.files['profilepic']
            fileName = secure_filename(file.filename)
            imageHandler.dogImageHandler(file, fileName)

            dogData = (
                request.form['name'],
                request.form['birthday'],
                fileName,
                request.form['race'],
                request.form['character'],
                session['id']
            )

            dataHandler.insertDogData(dogData)

            return redirect("/user/profile")
        if session.get('loggedin') == True:   
            return render_template("addDog.html")
        else:
            return redirect("/dashboard")
