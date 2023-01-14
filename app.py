import os

from dotenv import load_dotenv
from flask_cors import CORS
from flask_restful import Api

from src.config import app
from src.resources.ad import CreateAd, GetAd
from src.schema.schema import db

load_dotenv()

DEBUG_MODE = os.environ.get('DEBUG', True)

CORS(app)

api = Api(app)

api.add_resource(CreateAd, '/submit')
api.add_resource(GetAd, '/get')

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)
