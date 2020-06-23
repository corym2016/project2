# This is your classes and tables for your database

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    u_id = db.Column(db.Integer, primary_key=True)
    u_username= db.Column(db.String, nullable=False)
    u_password = db.Column(db.String, nullable=False)
    u_firstname = db.Column(db.String, nullable=False)
    u_lastname = db.Column(db.String, nullable=False)
