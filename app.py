import os
import json

from dotenv import load_dotenv
from flask_cors import CORS
from flask_restful import Api

from src.config import app
from src.resources.ad import CreateAd, GetAd

load_dotenv()

DEBUG_MODE = os.environ.get('DEBUG', True)
TRUSTED_USERS = {key, value for key, value in json.loads(os.environ.get('TRUSTED_USERS', {})}

CORS(app)

api = Api(app)

api.add_resource(CreateAd, '/submit')
api.add_resource(GetAd, '/get')

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)
