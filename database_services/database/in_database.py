import os
import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import py_logging

from database_services.database_objects.item import Item
from database_services.database_objects.price import Price
from get_config import get_config


def item_in_database(item: Item, session_lock: threading.Lock) -> bool:
    config = get_config()
    engine = create_engine(
        '{}:///{}{}'.format(
            config['DEFAULT']['DatabaseType'], "C:\\Anthony\\Programs\\runescape-grand-exchange-data-analytics\\database_services\\database\\", config['DEFAULT']['DatabaseName']))
    Session = sessionmaker(bind=engine)

    logger = py_logging.create_logger(
        "item_in_database", '{}in_database.log'.format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    with session_lock:
        session = Session()
        is_in_database = bool(session.query(Item).filter(Item.item_id == item.item_id).count)
        session.close()
    logger.debug("{} is in database: {}".format(item.item_id, is_in_database))
    return is_in_database


def item_id_in_database(item_id: int, session_lock: threading.Lock) -> bool:
    config = get_config()
    engine = create_engine(
        '{}:///{}{}'.format(
            config['DEFAULT']['DatabaseType'], "C:\\Anthony\\Programs\\runescape-grand-exchange-data-analytics\\database_services\\database\\", config['DEFAULT']['DatabaseName']))
    Session = sessionmaker(bind=engine)

    logger = py_logging.create_logger(
        "item_id_in_database", '{}in_database.log'.format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    with session_lock:
        session = Session()
        count = session.query(Item).filter(Item.item_id == item_id).count()
        session.close()
    logger.debug("Number of {} in database: {}".format(item_id, count))
    return bool(count)
