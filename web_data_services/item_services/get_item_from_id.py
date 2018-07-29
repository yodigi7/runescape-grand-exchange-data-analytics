import requests
import py_logging
import os
from database_services.database_objects.item import Item
from database_services.database_objects.price import Price
from get_config import get_config


def get_item_runescape_url():
    config = get_config()
    return config['DEFAULT']['ItemRunescapeBaseUrl']


def get_item_from_id(id: int) -> Item:
    logger = py_logging.create_logger('get_item_from_id', '{}get_item__from_id.log'
                                      .format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    response = requests.get('{}{}'.format(get_item_runescape_url(), id)).json()
    name = response['item']['name']
    type = response['item']['type']
    description = response['item']['description']
    is_members_only = response['item']['members']
    logger.info('ID = {} and name = {}'.format(id, name))
    return Item(item_id=id, name=name, type=type, is_members_only=is_members_only, description=description)


if __name__ == '__main__':
    print(get_item_from_id(24372))
