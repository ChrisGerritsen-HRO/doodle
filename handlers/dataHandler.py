import sqlite3

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