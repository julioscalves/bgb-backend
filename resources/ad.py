from datetime import datetime
from flask import request
from flask_restful import Resource

from src.config import TIMEBLOCK
from src.schema.schema import Ad, User, db
from src.resources.utils.tag import generate_tag
from src.resources.utils.utils import format_index


class CreateAd(Resource):
    """
        Handles the ad creation process.
        Note to self: Consider writing a new class
        for auctions.
    """

    @staticmethod
    def register_user(userid: str, username: str, blocked_until: int) -> None:
        """
        If the user is not registered, a new user should
        be created.

        Args:
            userid (str): _description_
            username (str): _description_
            blocked_until (int): _description_
        """
        new_user = User(id=userid,
                        username=username,
                        is_banned=False,
                        blocked_until=blocked_until)
        db.session.add(new_user)

    @staticmethod
    def can_user_send_message(user: str) -> bool:
        """
            Checks if the user is allowed to send a message.

        Args:
            user (str): user id

        Returns:
            bool: allowed or not.
        """
        user_query = User.query.filter_by(id=user).first()

        return True if user_query is None else user_query.blocked_until > datetime.now(
        )

    @staticmethod
def group_by_type(data: dict) -> str:
    groups = {i: [] for i in range(5)}  # simplified dictionary initialization
    message = ''

    for item in data:
        groups[item['type']].append(item)

    group_map = {
        0: '💵 #VENDO',
        1: '⚖️ #VENDO OU #TROCO',
        2: '🤝 #TROCO',
        3: '🔨 #LEILÃO',
        4: '🔎 #PROCURO'
    }

    for group in groups:
        item_list = groups[group]
        
        if not item_list:  # use boolean evaluation to check if list is empty
            continue
        
        message += f'{group_map[group]}\n\n'
        
        for index, item in enumerate(item_list, start=1):
            tag = generate_tag(item['name'])
            message += f'\t\t➤ #{index} {tag}'
            
            if item['type'] <= 1:
                message += f' R$ {item["price"]}'
            
            if item['description']:
                description = item['description'].replace("\n", ". ")
                message += f'\n       {description}'
            
            message += '\n'
        
        message += '\n'

    return message
    def post(self):
        userid = request.json.get('id')

        if self.can_user_send_message(userid):
            pass


class GetAd(Resource):

    def post(self):
        print(self)
