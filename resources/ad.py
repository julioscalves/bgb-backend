from flask import request
from flask_restful import Resource

from src.schema.schema import Ad, User


class CreateAd(Resource):

    def post(self):
        print(request.json)


class GetAd(Resource):

    def post(self):
        print(self)
