import os.path
from flask import Flask, request, redirect,render_template
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate, migrate
#from flask.templating import render_template
import sys

app =  Flask(__name__)

#this line connect to the db and create new db (table?) named registrations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations.db'
#initializes a database object named db using the SQLAlchemy library in Python.
db = SQLAlchemy(app)

class Registration(db.Model):
    #all of thw bellow are the table column
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(15), nullable=False)

    def __repr__(self) -> str:
        return super().__repr__()


@app.route('/')
def projectIntro():
    return render_template("Introduction.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("fullname")
        email = request.form.get("email")
        #creatiing new table named registration 
        registration = Registration(full_name=full_name, email=email)
        db.session.add(registration)
        db.session.commit()
        return redirect("/Welcome?fullname=" + full_name)
    return render_template("signup.html")


@app.route('/Welcome')
def hello_user():
    full_name = request.args.get("fullname")
    return render_template("Welcome.html", fullname=full_name)


if __name__ == '__main__':
   with app.app_context():
       db.create_all()
   app.run(host="0.0.0.0", port=5000)

