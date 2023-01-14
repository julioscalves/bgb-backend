from datetime import datetime
from flask_restful import Resource

from src.schema.schema import User
from src.resources.utils.messages import assemble_message


class Authentication(Resource):

    @staticmethod
    def repack_auth_data(data):
        repacked_data = {
            'id': data.get('id', None),
            'first_name': data.get('first_name', None),
            'last_name': data.get('last_name', None),
            'username': data.get('username', None),
            'photo_url': data.get('photo_url', None),
            'auth_date': data.get('auth_date', None),
            'hash': data.get('hash', None)
        }

        return repacked_data

    def post(self, data):
        authentication_data = self.repack_auth_data(data)

        if authentication_data['id'] is None:
            return assemble_message(key='invalid_id')

        elif authentication_data['username'] is None:
            return assemble_message(key='invalid_username')

        user = User.query.filter_by(id=authentication_data['id']).first()

        if user:
            block = user.blocked_until

            if not block < datetime.now():
                return assemble_message(
                    key='blocked',
                    message=
                    f'Você só poderá enviar uma nova mensagem após {block.strftime("%d/%m às %H:%Mh")}.',
                    replace=True)

            if user.is_banned:
                return assemble_message(key='banned')
