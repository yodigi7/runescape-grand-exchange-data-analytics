import sqlite3
import threading

import sqlalchemy

import py_logging
from json import JSONDecodeError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_services.add_item_to_database_by_id import add_item_to_database_by_id_thread
from database_services.database.in_database import item_id_in_database
from web_data_services.top_items.get_top_price_categories import *
from web_data_services.item_services.get_item_from_id import *
from web_data_services.item_services.get_id_from_name import *


def add_all_top_price_items():
    print(threading.get_ident())
    config = get_config()
    engine = create_engine(
        ':///database_services\\database\\'.join([config['DEFAULT']['DatabaseType'], config['DEFAULT']['DatabaseName']]))
    Session = sessionmaker()
    session = Session(bind=engine)

    lock = threading.Lock()
    threads = []
    names = get_top_price_fall_names()[:5]  # + get_top_price_rise_names() + get_top_price_value_names()

    for name in names:
        item = get_item_from_id(
                    get_id_from_name(name))
        thread = threading.Thread(target=item.add_to_database_thread, args=(lock,))
        thread.start()
        threads.append(thread)

    return threads


def add_all_top_price_items_thread(session_lock: threading.Lock, get_lock: threading.Lock = None):
    print(threading.get_ident())
    # logger = py_logging.create_logger(
    #     'add_all_top_price_items_thread', '{}add_all_top_price_items.log'
    #         .format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    threads = []
    names = get_top_price_fall_names()[:5]  # + get_top_price_rise_names() + get_top_price_value_names() + get_top_price_most_traded_names()
    print(names)
    if not get_lock:
        get_lock = threading.Lock()

    for name in names:
        print(name)
        id = get_id_from_name(name)
        if item_id_in_database(id, session_lock):
            # logger.info("{} is already in the database".format(name))
            print("{} is already in the database".format(name))
            continue
        print("After")
        if id is None:
            # logger.warning("Couldn't find ID for: {}".format(name))
            print("Couldn't find ID for: {}".format(name))
            continue
        threads.append(
            threading.Thread(target=add_item_to_database_by_id_thread, args=(id, session_lock, get_lock)))

    print("Starting threads")
    print(threads)
    for thread in threads:
        print("starting thread...")
        thread.start()
    print("JOINING THREADS")
    for thread in threads:
        thread.join()


def func():
    print(threading.get_ident())
    lock = threading.Lock()
    # add_all_top_price_items_thread(lock)
    thread = threading.Thread(target=add_all_top_price_items_thread, args=(lock,))
    thread.start()


if __name__ == '__main__':
    lock = threading.Lock()
    # add_all_top_price_items_thread(lock)
    thread = threading.Thread(target=add_all_top_price_items_thread, args=(lock,))
    thread.start()
    thread.join()
