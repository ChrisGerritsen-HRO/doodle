from flask import Flask, request, url_for, session
import flask
from flask.helpers import flash
from flask.templating import render_template
from werkzeug.utils import redirect, secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os, re

# Import dataHandler
from handlers.userDataHandler import dataHandler
# Import imageHandler
from handlers.imageHandler import imageHandler

SECRET_KEY = os.urandom(24)
DATABASE = 'doodle.db'
UPLOADFOLDER = 'static/user'
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

class user():

    def login():
        msg = ''
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            sqlConnection = sqlite3.connect(DATABASE)
            cursor = sqlConnection.cursor()
            userSelect = """SELECT * FROM user WHERE email = ?"""
            cursor.execute(userSelect, (email, ))
            user = cursor.fetchone()

            checkPasswrd = check_password_hash(user[5], password)

            if user:
                if checkPasswrd:
                    session['loggedin'] = True
                    session['id'] = user[0]
                    session['name'] = user[1]
                    session['email'] = user[2]
                    session['birthday'] = user[3]
                    session['profilepic'] = user[4]
                    return redirect("/dashboard")
                else:
                    msg = 'Email of wachtwoord is onjuist!'

        if session.get('loggedin') != True:            
            return render_template("login.html", msg = msg)
        else:
            return redirect("/dashboard")
    
    def logout():
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('name', None)
        session.pop('email', None)
        session.pop('birthday', None)
        session.pop('profilepic', None)
        return redirect("/")

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
        if session.get('loggedin') != True:   
            return render_template("register.html", msg = msg)
        else:
            return redirect("/dashboard")

    def profile():
        if session.get('loggedin') == True:
            userData = dataHandler.selectUserData()
            return render_template("profile.html", userData = userData)
        else:
            return redirect("/login")

    def editUserProfile():
        if request.method == "POST":
            file = request.files['profilepic']
            fileName = secure_filename(file.filename)
            if file.tell() != 0:
                file = request.files['profilepic']
                fileName = secure_filename(file.filename)
                imageHandler.userImageHandler(file, fileName)

            updatedUserData = ()

            userData = dataHandler.selectUserData()
            print(userData)
            if request.form['name'] != '':
                updatedUserData = updatedUserData + (request.form['name'], )
            else:
                updatedUserData = updatedUserData + (userData['name'], )
            if request.form['email'] != '':
                updatedUserData = updatedUserData + (request.form['email'], )
            else:
                updatedUserData = updatedUserData + (userData['email'], )
            if request.form['birthday'] != '':
                updatedUserData = updatedUserData + (request.form['birthday'], )
            else:
                updatedUserData = updatedUserData + (userData['birthday'], )
            if fileName != '':
                updatedUserData = updatedUserData + (fileName, )
            else:
                updatedUserData = updatedUserData + (userData['profilepic'], )
            if request.form['password'] != '':
                hashPasswrd = generate_password_hash(request.form['password'], "sha256")
                updatedUserData = updatedUserData + (hashPasswrd, )
            else:
                updatedUserData = updatedUserData + (userData['password'], )
            updatedUserData = updatedUserData + (session['id'], )

            # hashPasswrd = generate_password_hash(request.form['password'], "sha256")
            # updatedUserData = (
            #     request.form['name'],
            #     request.form['email'],
            #     request.form['birthday'],
            #     fileName,
            #     hashPasswrd,
            #     session['id']
            # )

            dataHandler.updateUserData(updatedUserData)

            return redirect("/")
        if session.get('loggedin') == True:
            userData = dataHandler.selectUserData()
            return render_template("editUserProfile.html", userData = userData)
        else:
            return redirect("/login")