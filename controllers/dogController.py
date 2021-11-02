from flask import Flask, request, url_for, session
import flask
from flask.helpers import flash
from flask.templating import render_template
from werkzeug.utils import redirect, secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os, re

# Import dataHandler
from handlers.dogDataHandler import dogDataHandler
# Import imageHandler
from handlers.imageHandler import imageHandler
from handlers.userDataHandler import dataHandler

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

            dogDataHandler.insertDogData(dogData)

            return redirect("/user/profile")
        if session.get('loggedin') == True:   
            return render_template("addDog.html")
        else:
            return redirect("/dashboard")

    def dogProfile(name):
        if session.get('loggedin') == True:
            dogData = dogDataHandler.selectDog(name)
            return render_template("dogProfile.html", dogData = dogData)
        else:
            return redirect("/login")

    def editDogProfile(name):
        if request.method == "POST":
            file = request.files['profilepic']
            fileName = secure_filename(file.filename)

            updatedDogData = ()

            dogData = dogDataHandler.selectDog(name)
            if request.form['name'] != '':
                updatedDogData = updatedDogData + (request.form['name'], )
            else:
                updatedDogData = updatedDogData + (dogData['name'], )
            if request.form['birthday'] != '':
                updatedDogData = updatedDogData + (request.form['birthday'], )
            else:
                updatedDogData = updatedDogData + (dogData['birthday'], )
            if request.form['race'] != '':
                updatedDogData = updatedDogData + (request.form['race'], )
            else:
                updatedDogData = updatedDogData + (dogData['race'], )
            if request.form['character'] != '':
                updatedDogData = updatedDogData + (request.form['character'], )
            else:
                updatedDogData = updatedDogData + (dogData['character'], )
            if fileName != '':
                file = request.files['profilepic']
                fileName = secure_filename(file.filename)
                imageHandler.dogImageHandler(file, fileName)
                updatedDogData = updatedDogData + (fileName, )
            else:
                updatedDogData = updatedDogData + (dogData['profilepic'], )
            updatedDogData = updatedDogData + (dogData['id'], )
                
            dogDataHandler.updateDogData(updatedDogData)

            return redirect("/")
        if session.get('loggedin') == True:
            dogData = dogDataHandler.selectDog(name)
            return render_template("editDogProfile.html", dogData = dogData)
        else:
            return redirect("/login")
