from datetime import datetime
from flask import request
from flask_restful import Resource

from src.config import TIMEBLOCK
from src.schema.schema import Ad, User, db
from src.resources.utils.tag import generate_tag
from src.resources.utils.utils import format_index


class CreateAd(Resource):

    @staticmethod
    def can_user_send_message(user: str) -> bool:
        user_query = User.query.filter_by(id=user).first()
        return True if user_query is None else user_query.blocked_until > datetime.now(
        )

    @staticmethod
    def register_user(userid: str, username: str, blocked_until: int) -> None:
        new_user = User(id=userid,
                        username=username,
                        is_banned=False,
                        blocked_until=blocked_until)
        db.session.add(new_user)

    @staticmethod
    def group_by_type(data: dict) -> str:
        groups = {
            0: [],  #only sell
            1: [],  #sell or tarde
            2: [],  #only trade
            3: [],  #auction
            4: [],  #looking for
        }
        message = ''

        for item in data:
            item_type = item['type']
            groups[item_type].append(item)

        group_map = {
            0: '💵 #VENDO',
            1: '⚖️ #VENDO OU #TROCO',
            2: '🤝 #TROCO',
            3: '🔨 #LEILÃO',
            4: '🔎 #PROCURO'
        }

        index = 1

        for group in groups.keys():
            if len(groups[group]) > 0:
                item_list = groups[group]
                message += f'{group_map[group]}\n\n'

                for item in item_list:
                    tag = generate_tag(item['name'])
                    message += f'\t\t➤ #{format_index(index)} {tag}'

                    if item['type'] <= 1:
                        message += f' R$ {item["price"]}'

                    if len(item['description']) > 0:
                        new_line = '\n       '
                        message += f'{new_line}{item["description"].replace(new_line, ". ")}'

                message += '\n'

            message += '\n'

        return message

    def post(self):
        print(request.json)


class GetAd(Resource):

    def post(self):
        print(self)
