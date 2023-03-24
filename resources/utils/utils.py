import difflib
import json
import string
import random
import requests

from src.config import DEFAULT_MESSAGE_PARAMS, EDIT_MESSAGE_URL, SUBMIT_MESSAGE_URL
from src.schema.schema import Ad


def generate_random_id(length=8):
    digits = string.digits
    identifier = [random.choice(digits) for _ in range(length)]
    identifier.insert(4, '.')

    collision_check = Ad.query.filter_by(id=''.join(identifier)).all()

    if collision_check:
        identifier = generate_random_id()

    return ''.join(identifier)


def unpack_json(data: dict, level=0) -> None:
    print('*' * 25)

    for key, value in data.items():
        if isinstance(value, dict):
            print('\t' * level, f'{key}:')
            unpack_json(value, level + 1)
        else:
            print('\t' * level, f'{key}: {value}')

    print('*' * 25)


def format_index(index: int) -> str:
    return str(index).zfill(2)


def unpack_command_and_arguments(text: str) -> list:
    command, *arguments = text.split()

    return command, arguments


def unpack_massage_data(key: str, data: dict) -> list:
    if 'reply_to_message' not in data[key]:
        return []

    reply_data = data[key]['reply_to_message']
    message = reply_data.get('text', '')
    message_id = reply_data.get('forward_from_message_id', '')
    chat_message_id = reply_data.get('message_id', '')
    infos = message.split('\n\n')
    user = data[key]['from'].get('username', '')

    return [message, message_id, chat_message_id, infos, user]


def fix_target(text: str) -> str:
    return '#' + text.strip('#') + ' '


def format_price(text: str) -> str:
    text = text.replace('.', '')

    if ',' not in text:
        text = text + ',00'

    if '.' not in text and len(text) > 6:
        text = text[:-6] + '.' + text[-6:]

    return text


def replace_last_comma(text: str) -> str:
    comma_index = text.rfind(',')
    text = text[:comma_index] + ' e' + text[comma_index + 1:].rstrip()

    return text


def remove_duplicates(items: list) -> list:
    return sorted(set(items))


def calculate_similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def is_the_same_message(message: str):
    for ad in Ad.query.order_by(Ad.id).all():
        similarity = calculate_similarity(json.dumps(message),
                                          json.dumps(ad.content))

        if similarity == 1:
            return ad.id

    return None


def post_message(data: dict, method: str) -> None:
    urls = {'submit': SUBMIT_MESSAGE_URL, 'edit': EDIT_MESSAGE_URL}
    payload = {**DEFAULT_MESSAGE_PARAMS, **data}
    response = requests.post(urls[method], data=payload)

    return unpack_json(response)
