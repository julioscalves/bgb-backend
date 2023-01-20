import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()

TIMEBLOCK = os.environ.get('TIMEBLOCK')
DB_PATH = f"{os.environ.get('DB_FOLDER')}/{os.environ.get('DB_FILENAME')}.db"

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.getcwd(), DB_PATH)}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
