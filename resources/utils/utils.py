import string
import random

from src.schema.schema import Ad


def generate_random_id(length=8):
    """
        Generates a unique random id for each ad.
    """

    digits = string.digits
    identifier = [random.choice(digits) for _ in range(length)]
    identifier = ''.join(identifier[:4] + ['.'] + identifier[4:])

    collision_check = Ad.query.filter_by(id=id).all()

    if collision_check:
        identifier = generate_random_id()

    return identifier


def unpack_json(data: dict) -> None:
    """
        Unpacks json data for logging purposes.
    """

    print('*' * 25)

    for key in data.keys():
        if isinstance(data[key], dict):
            unpack_json(data[key])

        print(f'{key}: {data[key]}')

    print('*' * 25)


def format_index(index: int) -> str:
    index = str(index) if index > 9 else f'0{index}'

    return index
