import sqlite3

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_services.database_objects.item import Item
from database_services.database_objects.price import Price
from get_config import get_config
from web_data_services.item_services.get_id_from_name import get_id_from_name
from web_data_services.item_services.get_item_from_id import get_item_from_id


# TODO: Delete this whole file or repurpose it
# This is just to mess around and to make sure that everything works


Session = sessionmaker()


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
    config = get_config()
    engine = create_engine(':///database_services\\database\\'.join([config['DEFAULT']['DatabaseType'], config['DEFAULT']['DatabaseName']]))
    Session = sessionmaker(Session)
    session = Session(bind=engine)
    Item(item_id=5797, name="name", description="description", type="type").add_to_database(session)
    # Price(item_id=5797, runescape_time=12378).add_to_database(session)
