from flask import request
from flask_restful import Resource

from src.schema.schema import Ad, User
from src.resources.utils.tag import generate_tag
from src.resources.utils.utils import format_index


class CreateAd(Resource):

    @staticmethod
    def group_by_type(data: dict) -> str:
        groups = {
            'Apenas Venda': [],
            'Apenas Troca': [],
            'Venda ou Troca': [],
            'Leilão Externo': [],
            'Procura': [],
        }
        message = ''

        for item in data:
            item_type = item['type']
            groups[item_type].append(item)

        group_map = {
            'Apenas Venda': '💵 #VENDO',
            'Apenas Troca': '🤝 #TROCO',
            'Venda ou Troca': '⚖️ #VENDO OU #TROCO',
            'Leilão Externo': '🔨 #LEILÃO',
            'Procura': '🔎 #PROCURO'
        }

        index = 1

        for group in groups.keys():
            if len(groups[group]) > 0:
                item_list = groups[group]
                message += f'{group_map[group]}\n\n'

                for item in item_list:
                    tag = generate_tag(item['name'])
                    message += f'\t\t➤ #{format_index(index)} {tag}'

                    if item['type'].lower() == 'apenas venda' or item[
                            'type'].lower() == 'venda ou troca':
                        message += f' R$ {item["price"]}'

                    if len(item['description']) > 0:
                        message += f'\n       {item["description"].replace("\n", ". ")}'

                message += '\n'

            message += '\n'

        return message

    def post(self):
        print(request.json)


class GetAd(Resource):

    def post(self):
        print(self)
