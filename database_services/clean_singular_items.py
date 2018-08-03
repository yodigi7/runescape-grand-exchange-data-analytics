import sqlite3

import requests
import multiprocessing
import json
import time

from database_services.database.in_database import get_singular_ids_in_database

import sqlalchemy

import py_logging
from database_services.database.in_database import get_ids_in_database, determine_new_days
from database_services.database_objects.price import Price, add_all_to_database
from database_services.database_objects.item import Item
from get_processors import get_number_of_processors_running


def clean_singular_items(session_lock: multiprocessing.Lock) -> None:
    for item in get_singular_ids_in_database(session_lock):
        item.delete_in_database(session_lock)


if __name__ == '__main__':
    pass
