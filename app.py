from flask import Flask, request,url_for
from flask.templating import render_template
from werkzeug.utils import redirect
import sqlite3

app = Flask(__name__)

DATABASE = 'doodle.db'

@app.route("/")
def main():
    return "<p>Index page!</p>"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            nm = request.form['name']
            email = request.form['email']
            birthday = request.form['birthday']
            profilePic = request.form['profilepic']
            passwrd = request.form['password']
            confirmPasswrd = request.form['confirmpass']

            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user (name, email, birthday, profilepic, password, confirmpass) VALUES (?,?,?,?,?,?)", (nm, email, birthday, profilePic, passwrd, confirmPasswrd))
                
                con.commit()
        except:
            pass
        finally:
            con.close()
            return redirect(url_for(main))

    return render_template("register.html")
