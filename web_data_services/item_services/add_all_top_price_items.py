import sqlite3
import multiprocessing

import sqlalchemy

import py_logging
from json import JSONDecodeError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_services.add_item_to_database_by_id import add_item_to_database_by_id_thread
from database_services.database.in_database import is_item_name_in_database
from database_services.session_controller import shared_session
from web_data_services.top_items.get_top_price_categories import *
from web_data_services.item_services.get_item_from_id import *
from web_data_services.item_services.get_id_from_name import *


def add_all_top_price_items():
    # print(threading.get_ident())

    lock = multiprocessing.Lock()
    processes = []
    names = get_top_price_fall_names() + get_top_price_rise_names() + get_top_price_value_names() + get_top_price_most_traded_names()

    for name in names:
        item = get_item_from_id(
                    get_id_from_name(name))
        process = multiprocessing.Process(target=item.add_to_database_thread, args=(lock,))
        process.start()
        processes.append(process)

    return processes


def add_all_top_price_items_thread(session_lock: multiprocessing.Lock, get_lock: multiprocessing.Lock = None):
    # print(threading.get_ident())
    logger = py_logging.create_logger(
        'add_all_top_price_items_thread', '{}add_all_top_price_items.log'
        .format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    processes = []
    names = get_top_price_fall_names() + get_top_price_rise_names() + get_top_price_value_names() + get_top_price_most_traded_names()
    print(names)
    if not get_lock:
        get_lock = multiprocessing.Lock()

    for name in names:
        print(name)
        if is_item_name_in_database(name, session_lock):
            logger.info("{} is already in the database".format(name))
            print("{} is already in the database".format(name))
            continue
        id = get_id_from_name(name)
        if id is None:
            logger.warning("Couldn't find ID for: {}".format(name))
            print("Couldn't find ID for: {}".format(name))
            continue
        print("ID: {}".format(id))
        process = multiprocessing.Process(target=add_item_to_database_by_id_thread, args=(id, session_lock, get_lock))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    process = multiprocessing.Process(target=add_all_top_price_items_thread, args=(lock,))
    process.start()
