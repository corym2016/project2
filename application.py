import os, json
import requests

from flask import Flask, session, redirect, render_template, request, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_socketio import SocketIO, emit

from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL"))

# create a 'scoped session' that ensures different users' interactions with the
# database are kept separate
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
#@login_required
def index():
    return render_template("index.html")

@app.route("/Credentials", methods=["POST"])
def open():
    if request.form['creds'] == 'login':
        return render_template("login.html")
    else:
        return render_template("register.html")

@app.route("/Login", methods=["POST", "GET"])
def login():
    """Sign In Here."""
    # forget user data
    session.clear()
    # Get form username.
    username = request.form.get("username")
    # Check to make sure username exists
    user = db.execute("SELECT * FROM users WHERE u_username = :username", {"username": username}).fetchone()
    if user is None:
        return render_template("sign_in.html", message="*Username does not exist.")
    else:
        if user == None or not check_password_hash(user[2], request.form.get("password")):
            return render_template("login.html", message="*Password incorrect.")
        else:
            # making the session (I think???)
            session['user_id'] = user[0]
            session['username'] = user[1]
            # Sending users data to next page
            return render_template("profile.html", user=user, message="Successfully signed in.")

@app.route('/Logout')
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/Register", methods=["GET", "POST"])
def register():
    """Register Here."""
    # clear session data
    session.clear()
    # Get form information.
    username = request.form.get("username")
    password = request.form.get("password")
    con_password = request.form.get("con_password")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    # Check to make sure username is not alread taken.
    usercheck = db.execute("SELECT * FROM users WHERE u_username = :username", {"username":username}).fetchone()
    if usercheck is None:
        if password == con_password:
            # Hash password to store
            hashPass = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            # Add that users info to the database
            db.execute("INSERT INTO users (u_username, u_password, u_firstname, u_lastname) VALUES (:username, :hashPass, :firstname, :lastname)", {"username":username, "hashPass":hashPass, "firstname":firstname, "lastname":lastname})
            db.commit()
            return render_template("login.html", message="Succesfully registered, please sign in.")
        else:
            return render_template("register.html", message="*Passwords do not match. Please try again.")
    else:
        return render_template("register.html", message="*Username already taken, please choose a different username.")

texts = ["Chat Room 1", "Chat Room 2", "Chat Room 3"]
mes1 = ["Hello"]
mes2 = []
mes3 = []

@app.route("/Room1")
def room1():
    return texts[0]
    return mes1

@app.route("/Room2")
def room2():
    return texts[1]

@app.route("/Room3")
def room3():
    return texts[2]

@socketio.on("submit vote")
def vote(data):
    selection = data["selection"]
    votes[selection] += 1
    emit("vote totals", votes, broadcast=True)
