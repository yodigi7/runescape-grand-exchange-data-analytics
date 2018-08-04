import sqlite3

import multiprocessing
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clean_singular_items import clean_singular_items
from database_services.database_objects.item import Item
from database_services.database_objects.price import Price
from get_config import get_config
from web_data_services.historic_prices.get_historic_prices import get_all_historic_prices
from web_data_services.item_services.add_all_top_price_items import add_all_top_price_items_thread
from web_data_services.item_services.get_id_from_name import get_id_from_name
from web_data_services.item_services.get_item_from_id import get_item_from_id

# TODO: Delete this whole file or repurpose it
# This is just to mess around and to make sure that everything works


def get_names_to_add_to_database():
    Session = sessionmaker()
    engine = create_engine('sqlite:///database_services/database/runescape-grand-exchange-data.db')
    session = Session(bind=engine)
    print(session.query(Item).count())
    exit()
    while True:
        name = input("Enter a name to add to the Items database: ")
        try:
            get_item_from_id(
                get_id_from_name(name)).add_to_database(session)
        except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError):
            session.rollback()
            print("Sorry, {} is already part of the database".format(name))
        except RuntimeError as e:
            print(str(e))


if __name__ == '__main__':
    session_lock = multiprocessing.Lock()
    runescape_lock = multiprocessing.Lock()
    add_all_top_price_items_thread(session_lock, runescape_lock)
    clean_singular_items(session_lock)
    get_all_historic_prices(session_lock, runescape_lock)
