import threading
import time
from json import JSONDecodeError

import requests
import py_logging
import os
from database_services.database_objects.item import Item
from database_services.database_objects.price import Price
from get_config import get_config


def get_item_runescape_url():
    config = get_config()
    return config['DEFAULT']['ItemRunescapeBaseUrl']


def get_item_from_id(id: int, lock: threading.Lock = None) -> Item:
    logger = py_logging.create_logger('get_item_from_id', '{}get_item__from_id.log'
                                      .format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    if lock is not None:
        with lock:
            response = requests.get('{}{}'.format(get_item_runescape_url(), id)).json()
    else:
        response = requests.get('{}{}'.format(get_item_runescape_url(), id)).json()
    name = response['item']['name']
    type = response['item']['type']
    description = response['item']['description']
    is_members_only = True if response['item']['members'] == 'true' else False
    logger.info('ID = {} and name = {}'.format(id, name))
    return Item(item_id=id, name=name, type=type, is_members_only=is_members_only, description=description)


def get_item_from_id_thread(id: int, item: Item, get_lock: threading.Lock, delay=5) -> Item:
    logger = py_logging.create_logger('get_item_from_id', '{}get_item__from_id.log'
                                      .format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    with get_lock:
        try:
            response = requests.get(''.join([get_item_runescape_url(), str(id)])).json()
            time.sleep(delay)
        except JSONDecodeError:
            time.sleep(300)
            response = requests.get(''.join([get_item_runescape_url(), str(id)])).json()
            time.sleep(delay)
    name = response['item']['name']
    type = response['item']['type']
    description = response['item']['description']
    is_members_only = True if response['item']['members'] == 'true' else False
    logger.info('ID = {} and name = {}'.format(id, name))
    item.item_id = id
    item.name = name
    item.type = type
    item.is_members_only = is_members_only
    item.description = description
    return item


if __name__ == '__main__':
    print(get_item_from_id(24372))
