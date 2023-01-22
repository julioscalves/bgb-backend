import json
import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()

BGB_BAZAR_CHANNEL_ID = os.environ.get('BGB_BAZAR_CHANNEL_ID', None)
BGB_BAZAR_COMMENTS_ID = os.environ.get('BGB_BAZAR_COMMENTS_ID', None)
BOT_NAME = os.environ.get('BOT_NAME', None)
DB_PATH = f"{os.environ.get('DB_FOLDER')}/{os.environ.get('DB_FILENAME')}.db"
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', None)
TIMEBLOCK = os.environ.get('TIMEBLOCK', 1)

DEFAULT_MESSAGE_PARAMS = {
    'disable_web_page_preview': True,
    'parse_mode': 'HTML',
}
TRUSTED_USERS = {
    int(key): str(value)
    for key, value in json.loads(os.environ.get('TRUSTED_USERS', {})).items()
}

EDIT_MESSAGE_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/editMessageText'
SUBMIT_MESSAGE_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.getcwd(), DB_PATH)}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
