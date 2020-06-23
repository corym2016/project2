# use to create the necessary database tables
# grabbing objects from models
# run this before running application.py to ensure that tables are set in database

import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    # creating the tables
    db.create_all()
    db.session.commit()
    print('complete')

if __name__ == "__main__":
    with app.app_context():
        main()
