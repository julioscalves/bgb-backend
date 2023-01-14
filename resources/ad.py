from flask_restful import Resource

from src.schema.schema import Ad, User

class CreateAd(Resource):
    def post(self, data):
        print(self, data)


class GetAd(Resource):
    def get(self, data):
        pass
