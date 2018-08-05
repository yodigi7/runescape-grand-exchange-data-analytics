import os

import multiprocessing
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker

import py_logging

from database_services.session_controller import shared_session
from database_services.database_objects.item import Item
from database_services.database_objects.price import Price
from get_config import get_config


def is_item_in_database(item: Item, session_lock: multiprocessing.Lock) -> bool:
    logger = py_logging.create_logger(
        "item_in_database", '{}in_database.log'.format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    with session_lock:
        session = shared_session()
        is_in_database = bool(session.query(Item).filter(Item.item_id == item.item_id).count)
        session.close()
    logger.debug("{} is in database: {}".format(item.item_id, is_in_database))
    return is_in_database


def is_item_id_in_database(item_id: int, session_lock: multiprocessing.Lock) -> bool:
    logger = py_logging.create_logger(
        "is_item_id_in_database", '{}in_database.log'.format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    with session_lock:
        session = shared_session()
        count = session.query(Item).filter(Item.item_id == item_id).count()
        session.close()
    logger.debug("Number of {} in database: {}".format(item_id, count))
    return bool(count)


def is_item_name_in_database(name: str, session_lock: multiprocessing.Lock) -> bool:
    config = get_config()
    engine = create_engine(
        '{}:///{}{}'.format(
            config['DEFAULT']['DatabaseType'],
            "C:\\Anthony\\Programs\\runescape-grand-exchange-data-analytics\\database_services\\database\\",
            config['DEFAULT']['DatabaseName']))
    Session = sessionmaker(bind=engine)

    logger = py_logging.create_logger(
        "item_name_in_database", '{}in_database.log'.format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    with session_lock:
        session = Session()
        count = session.query(Item).filter(Item.name == name).count()
        session.close()
    logger.debug("Number of {} in database: {}".format(name, count))
    return bool(count)


def get_singular_ids_in_database(session_lock: multiprocessing.Lock) -> list:
    logger = py_logging.create_logger(
        "get_ids_in_database", '{}in_database.log'.format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    with session_lock:
        session = shared_session()
        return [x for x in session.query(Item).filter(
                or_(Item.name == "None",
                    Item.type == "None",
                    Item.is_members_only.is_(None),
                    Item.description == "None"))]


def get_ids_in_database(session_lock: multiprocessing.Lock) -> list:
    logger = py_logging.create_logger(
        "get_ids_in_database", '{}in_database.log'.format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    with session_lock:
        session = shared_session()
        return [x[0] for x in session.query(Item.item_id).distinct()]


def get_days_in_database(item_id: int, session_lock: multiprocessing.Lock) -> list:
    logger = py_logging.create_logger(
        "get_ids_in_database", '{}in_database.log'.format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    with session_lock:
        session = shared_session()
        return [x[0] for x in session.query(Price.runescape_time).filter(Price.item_id == item_id).distinct()]


def get_days_for_item(item_id: int, session_lock: multiprocessing.Lock) -> list:
    with session_lock:
        session = shared_session()
        return [x for x in session.query(Price.runescape_time, Price.price)
                .filter(Price.item_id == item_id).distinct()]


def determine_new_days(item_id: int, days: list, session_lock: multiprocessing.Lock) -> list:
    logger = py_logging.create_logger(
        "get_ids_in_database", '{}in_database.log'.format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    days_in_database = get_days_in_database(item_id, session_lock)
    print("Days in database: {}".format(days_in_database))
    return [x for x in days if x not in days_in_database]


if __name__ == '__main__':
    print(get_singular_ids_in_database(multiprocessing.Lock()))
