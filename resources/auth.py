import hashlib
import hmac

from datetime import datetime
from flask import jsonify
from flask_restful import Resource

from src.schema.schema import User
from src.resources.utils.messages import assemble_message


class Authentication(Resource):
    """
        Handles the authentication process.
    """

    @staticmethod
    def get_auth_data_string(data: dict) -> str:
        data_check_list = []

        for key in sorted(data.keys()):
            if data[key] is not None:
                data_check_list.append(key + '=' + str(data[key]))

        data_check = '\n'.join(data_check_list)

        return data_check

    @staticmethod
    def repack_auth_data(data: dict) -> dict:
        keys = [
            'id', 'first_name', 'last_name', 'username', 'photo_url',
            'auth_date', 'hash'
        ]
        repacked_data = {key: data.get(key, None) for key in keys}

        return repacked_data

    @staticmethod
    def authenticate(auth_data: dict, token: str) -> dict:
        for key in ['id', 'username']:
            if auth_data.get(key) is None:
                return assemble_message(key=f'invalid_{key}')

        user = User.query.filter_by(id=auth_data['id']).first()

        if user:
            if user.blocked_until and user.blocked_until > datetime.now():
                return assemble_message(
                    key='blocked',
                    message=
                    f'Você só poderá enviar uma nova mensagem após {user.blocked_until.strftime("%d/%m às %H:%Mh")}.',
                    replace=True)
            if user.is_banned:
                return assemble_message(key='banned')

        auth_hash = auth_data.pop('hash', None)
        auth_data_str = Authentication.get_auth_data_string(auth_data)
        token_secret_key = hashlib.sha256(token.encode()).digest()
        hmac_hash = hmac.new(token_secret_key,
                             msg=auth_data_str.encode(),
                             digestmod=hashlib.sha256).hexdigest()

        if hmac_hash != auth_hash:
            return assemble_message(key='invalid_hash')

        auth_timestamp = datetime.fromtimestamp(int(auth_data['auth_date']))
        expiration_time = datetime.now() - auth_timestamp

        if expiration_time.seconds > 86400:
            return assemble_message(key='expired_token')

        response = assemble_message(key='success')

        response['id'] = int(auth_data['id'])
        response['username'] = auth_data['username']
        response['first_name'] = auth_data['first_name']
        response['last_name'] = auth_data['last_name']
        response['hash'] = auth_hash
        response['auth_date'] = auth_data['auth_date']
        response['photo_url'] = auth_data['photo_url']

        return response

    def is_request_authentic(self, data: dict, token: str,
                             trusted_users: list) -> bool:
        user = data.json.get('user', None)

        if user in trusted_users:
            auth_data = data.json.copy()
            remove_keys = ['target_user', 'is_admin', 'status']

            for key in remove_keys:
                auth_data.pop(key, None)

            authentication = Authentication.authenticate(auth_data, token)

            return authentication['status'] == 'success'

        return False

    def post(self, data: dict, token: str) -> dict:
        auth_data = Authentication.repack_auth_data(data)
        response = Authentication.authenticate(auth_data, token)

        return jsonify(response)
