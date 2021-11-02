import sqlite3
from flask import Flask, request, url_for, session

from werkzeug.utils import redirect

DATABASE = 'doodle.db'  

class dataHandler():

    def insertDogData(dogData):
        try:
            sqlConnection = sqlite3.connect(DATABASE)
            cursor = sqlConnection.cursor()

            sqlite_insert_query = """INSERT INTO dog (name, birthday, profilepic, race, character, userID)
                                    VALUES 
                                    (?,?,?,?,?,?)"""
            
            cursor.execute(sqlite_insert_query, dogData)
            sqlConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to insert dog data", error)
        finally:
            if sqlConnection:
                sqlConnection.close()

    def selectUserDogs():
        sqlConnection = sqlite3.connect(DATABASE)
        cursor = sqlConnection.cursor()
        dogSelect = """SELECT * FROM dog WHERE id = ?"""
        cursor.execute(dogSelect, (session['id'], ))
        selectedDogData = cursor.fetchone()
        cursor.close()

        dogData = {
            'profilepic' : selectedDogData[4],
            'name' : selectedDogData[1],
            'email' : selectedDogData[2],
            'birthday' : selectedDogData[3],
            'password' : selectedDogData[5]
        }