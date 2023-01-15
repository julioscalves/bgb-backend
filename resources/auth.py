import difflib
import hashlib
import hmac
import json
import random
import re
import string

from datetime import datetime
from flask_restful import Resource

from src.schema.schema import User
from src.resources.utils.messages import assemble_message


class Authentication(Resource):
    """
        Handles authentication processes.
    """

    @staticmethod
    def get_authentication_data_string(data: dict) -> str:
        """Concatenates the authentication data into a string.

        Args:
            data (dict): authentication data

        Returns:
            str: authentication data string
        """
        data_check_list = []

        for key in sorted(data.keys()):
            if data[key] is not None:
                data_check_list.append(key + '=' + str(data[key]))

        data_check = '\n'.join(data_check_list)

        return data_check

    @staticmethod
    def repack_auth_data(data: dict) -> dict:
        """Repacks the authentication data.

        Args:
            data (dict): authentication data

        Returns:
            dict: repacked data
        """
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

    @staticmethod
    def authenticate(authentication_data: dict, token: str) -> dict:
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

        token_expiration_time = 86_400

        authentication_hash = authentication_data['hash']
        authentication_data.pop('hash', None)

        authentication_data_string = get_authentication_data_string(
            authentication_data)

        token_secret_key = hashlib.sha256(token.encode()).digest()
        hmac_hash = hmac.new(token_secret_key,
                             msg=authentication_data_string.encode(),
                             digestmod=hashlib.sha256).hexdigest()

        authentication_timestamp = datetime.fromtimestamp(
            int(authentication_data['auth_date']))
        now = datetime.now()

        authentication_timedelta = now - authentication_timestamp

        if hmac_hash != authentication_hash:
            return assemble_message(key='invalid_hash')

        elif authentication_timedelta.seconds > token_expiration_time:
            return assemble_message(key='expired_token')

        response = assemble_message(key='success')

        response['id'] = int(authentication_data['id'])
        response['username'] = authentication_data['username']
        response['first_name'] = authentication_data['first_name']
        response['last_name'] = authentication_data['last_name']
        response['hash'] = authentication_hash
        response['auth_date'] = authentication_data['auth_date']
        response['photo_url'] = authentication_data['photo_url']

        return response

    @staticmethod
    def is_request_authentic(data: dict, token: str, trusted_users: list) -> bool:
        user = data.json.get('user', None)

        if user in trusted_users:
            authentication_data = data.json.copy()
            remove_keys = ['target_user', 'is_admin', 'status']

            for key in remove_keys:
                authentication_data.pop(key, None)

            authentication = authenticate(authentication_data, token)

            return authentication['status'] = 'success'

        return False

    def post(self, data: dict, token: str) -> dict:
        authentication_data = self.repack_auth_data(data)
        response = authenticate(authentication_data)

        return response
