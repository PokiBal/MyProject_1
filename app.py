import os.path
from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
import sys

app =  Flask(__name__)

# db = SQLAlchemy(app)

# migrate = Migrate(app, db)
# class Profile(db.Model):
#     full_name = db.Column(db.String(20), unique=False, nullable=False)
#     def __str__(self):
#         return f"Name:{self.full_name}"

@app.route('/Welcome')
def hello_user():
    full_name = request.args.get("fullname")
    return render_template("Welcome.html", fullname=full_name)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("fullname")
        email = request.form.get("email")
        #p = Profile(_full_name=full_name, _email=email)
        return redirect("/Welcome?fullname=" + full_name)
    return render_template("signup.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
