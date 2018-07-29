import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from web_data_services.top_items.get_top_price_categories import *
from web_data_services.item_services.get_item_from_id import *
from web_data_services.item_services.get_id_from_name import *


def add_all_top_price_items():
    config = get_config()
    engine = create_engine(
        ':///database_services\\database\\'.join([config['DEFAULT']['DatabaseType'], config['DEFAULT']['DatabaseName']]))
    Session = sessionmaker()
    session = Session(bind=engine)

    lock = threading.Lock()
    threads = []
    names = get_top_price_fall_names() + get_top_price_rise_names() + get_top_price_value_names()

    for name in names:
        item = get_item_from_id(
                    get_id_from_name(name))
        thread = threading.Thread(target=item.add_to_database_thread, args=(session, lock,))
        thread.start()
        threads.append(thread)

    return threads


def add_all_top_price_items_thread(session, lock):
    threads = []
    names = get_top_price_fall_names() + get_top_price_rise_names() + get_top_price_value_names()

    for name in names:
        item = get_item_from_id(
                    get_id_from_name(name))
        thread = threading.Thread(target=item.add_to_database_thread, args=(session, lock,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    config = get_config()
    engine = create_engine(
        ':///database_services\\database\\'.join(
            [config['DEFAULT']['DatabaseType'], config['DEFAULT']['DatabaseName']]))
    Session = sessionmaker()
    session = Session(bind=engine)

    lock = threading.Lock()
    thread = threading.Thread(target=add_all_top_price_items_thread(session, lock))
    thread.start()
    thread.join()
