import os
import re
import requests
import utils

from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, redirect, jsonify
from flask.globals import request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


load_dotenv()

DB_PATH = f"{os.environ.get('DB_FOLDER')}/{os.environ.get('DB_FILENAME')}"

app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if not os.path.exists(DB_PATH):
    db.create_all()

from src.schema.schemas import Ad, User


@app.route('/get_ad', methods=['GET, POST'])
def get_ad():
    if request.is_json:
        pass