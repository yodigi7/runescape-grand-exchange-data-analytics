import configparser
import os
import requests
from database_services.database_objects.item import Item


def get_item_runescape_url():
    file = open(os.path.split(os.path.split(os.path.dirname(__file__))[0])[0] + os.sep + 'general.config')
    config = configparser.ConfigParser()
    config.read_file(file)
    return config['DEFAULT']['ItemRunescapeUrl']


def get_item_from_id(id: int) -> str:
    response = requests.get('{}{}'.format(get_item_runescape_url(), id)).json()
    name = response['item']['name']
    type = response['item']['type']
    description = response['item']['description']
    return Item(item_id=id, name=name, type=type, description=description)


if __name__ == '__main__':
    print(get_item_from_id(554))
