from web_data_services.item_services.get_item_from_id import get_item_from_id
from web_data_services.item_services.get_id_from_name import get_id_from_name
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sqlalchemy
import sqlite3
import json
from database_services.database_objects.item import Item



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
    get_names_to_add_to_database()
    # print(get_item_from_id(27512))
    # print(get_id_from_name("magic potion (4)"))
