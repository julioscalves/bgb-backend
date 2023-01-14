import os
import re
import requests

from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, redirect, jsonify
from flask.globals import request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from src.config import app
from src.schema.schema import db

load_dotenv()

DB_PATH = f"db/{os.environ.get('DB_FILENAME')}"
DEBUG_MODE = os.environ.get('DEBUG', True)

CORS(app)

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)
