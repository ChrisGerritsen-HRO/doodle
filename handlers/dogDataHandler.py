import sqlite3
from flask import Flask, request, url_for, session

from werkzeug.utils import redirect

DATABASE = 'doodle.db'  

class dogDataHandler():

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
        dogSelect = """SELECT * FROM dog WHERE userID = ?"""
        cursor.execute(dogSelect, (session['id'], ))
        selectedDogData = cursor.fetchall()
        cursor.close()

        print(selectedDogData)
        sqlConnection.close()
        return selectedDogData

    def selectDog(name):
        sqlConnection = sqlite3.connect(DATABASE)
        cursor = sqlConnection.cursor()
        dogSelect = """SELECT * FROM dog WHERE name = ?"""
        cursor.execute(dogSelect, (name, ))
        selectedDogData = cursor.fetchone()
        cursor.close()

        dogData = {
            'profilepic' : selectedDogData[3],
            'name' : selectedDogData[1],
            'birthday' : selectedDogData[2],
            'race' : selectedDogData[4],
            'character' : selectedDogData[5],
            'id' : selectedDogData[0]
        }

        print(dogData)
        sqlConnection.close()
        return dogData

    def updateDogData(dogData):
        try:  
            sqlConnection = sqlite3.connect(DATABASE)
            cursor = sqlConnection.cursor()

            sqlite_update_query = """ UPDATE dog
                                    SET name = ?,
                                    birthday = ?,
                                        race = ?,
                                        character = ?,
                                        profilepic = ?
                                    WHERE ID = ? """
            cursor.execute(sqlite_update_query, dogData)
            sqlConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to update user data", error)
        finally:
            if sqlConnection:
                sqlConnection.close()