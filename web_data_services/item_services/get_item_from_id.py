import requests

from database_services.database_objects.item import Item
from get_config import get_config


def get_item_runescape_url():
    config = get_config()
    print(list(config.sections()))
    print(list(config.keys()))
    print(list(config['DEFAULT'].keys()))
    return config['DEFAULT']['ItemRunescapeBaseUrl']


def get_item_from_id(id: int) -> str:
    response = requests.get('{}{}'.format(get_item_runescape_url(), id)).json()
    name = response['item']['name']
    type = response['item']['type']
    description = response['item']['description']
    return Item(item_id=id, name=name, type=type, description=description)


if __name__ == '__main__':
    print(get_item_from_id(554))
