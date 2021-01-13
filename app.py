import os
from flask import Flask, flash, request, redirect, url_for, render_template, flash, jsonify
import secrets
import random
import string

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import secretstuff

from datetime import datetime


# Define flask variables
app = Flask(__name__)
app.secret_key = secretstuff.secret_key
website_url = "http://localhost:5008/"

# DB initialisation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///findmyplanedb.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)


# Define DB models here

class Plane(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ident_public_key = db.Column(db.String)
    ident_private_key = db.Column(db.String)
    current_latitude = db.Column(db.Float)
    current_longitude = db.Column(db.Float)
    current_heading = db.Column(db.Integer)
    last_update = db.Column(db.DateTime)
    ever_received_data = db.Column(db.Boolean)

# API Endpoints

@app.route('/api/create_new_plane')
def api_new_plane():

    # Generate upper case random public key
    letters = string.ascii_uppercase
    public_key = ''.join(random.choice(letters) for i in range(5))

    # Generate random private key
    private_key = secrets.token_urlsafe(20)

    new_plane = Plane (
        ident_public_key = public_key,
        ident_private_key = private_key,
        current_latitude = 0,
        current_longitude = 0,
        current_heading = 0,
        last_update = datetime.utcnow(),
        ever_received_data = False
    )
    
    db.session.add(new_plane)
    db.session.commit()

    output_dictionary = {}
    output_dictionary["ident_public_key"] = public_key
    output_dictionary["ident_private_key"] = private_key

    return jsonify(output_dictionary)


@app.route('/api/update_plane_location', methods='[POST]')
def api_update_location():

    if request.method == 'POST':
        return "OK"
    
    else:
        return "POST method only please"


# The main event...

@app.route('/')
def index():
    return "Index"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
