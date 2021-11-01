import sqlite3
from flask import Flask, request, url_for, session

from werkzeug.utils import redirect

DATABASE = 'doodle.db'  


class dataHandler():

    def insertUserData(userData):
        try:
            sqlConnection = sqlite3.connect(DATABASE)
            cursor = sqlConnection.cursor()

            sqlite_insert_query = """INSERT INTO user (name, email, birthday, profilepic, password)
                                    VALUES 
                                    (?,?,?,?,?)"""
            
            cursor.execute(sqlite_insert_query, userData)
            sqlConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to insert user data", error)
        finally:
            if sqlConnection:
                sqlConnection.close()

    def selectUserData():
        sqlConnection = sqlite3.connect(DATABASE)
        cursor = sqlConnection.cursor()
        userSelect = """SELECT * FROM user WHERE id = ?"""
        cursor.execute(userSelect, (session['id'], ))
        selectedUserData = cursor.fetchone()
        cursor.close()

        userData = {
            'profilepic' : selectedUserData[4],
            'name' : selectedUserData[1],
            'email' : selectedUserData[2],
            'birthday' : selectedUserData[3],
            'password' : selectedUserData[5]
        }    
        print(userData)
        sqlConnection.close()
        return userData

    def updateUserData(userData):
        try:  
            sqlConnection = sqlite3.connect(DATABASE)
            cursor = sqlConnection.cursor()

            sqlite_update_query = """ UPDATE user
                                    SET name = ?,
                                    email = ?,
                                        birthday = ?,
                                        profilepic = ?,
                                        password = ?
                                    WHERE ID = ? """
            cursor.execute(sqlite_update_query, userData)
            sqlConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to update user data", error)
        finally:
            if sqlConnection:
                sqlConnection.close()