import sqlite3

import requests
import multiprocessing
import json
import time

import sqlalchemy

import py_logging
from database_services.database.in_database import get_ids_in_database, determine_new_days
from database_services.database_objects.price import Price, add_all_to_database
from database_services.database_objects.item import Item
from get_processors import get_number_of_processors_running


def get_historic_prices(item_ids: list, session_lock: multiprocessing.Lock, runescape_lock: multiprocessing.Lock) -> list:
    processes = []
    for item_id in item_ids:
        while get_number_of_processors_running(processes) >= multiprocessing.cpu_count():
            time.sleep(1)
        process = multiprocessing.Process(target=get_historic_prices_one_id, args=(item_id, session_lock, runescape_lock))
        process.start()
        processes.append(process)
    return processes


def get_historic_prices_one_id(item_id: int, session_lock: multiprocessing.Lock, runescape_lock: multiprocessing.Lock):
    with runescape_lock:
        # print("Got lock")
        response = requests.get("http://services.runescape.com/m=itemdb_rs/api/graph/{}.json".format(item_id))
        if len(response.text) is 0:
            print("Too many requests")
            time.sleep(60)
            json_response = requests.get("http://services.runescape.com/m=itemdb_rs/api/graph/{}.json".format(item_id)).json()
        else:
            json_response = response.json()
        # time.sleep(5)
    print("Starting to parse the data for {}".format(item_id))
    list_of_days = list(json_response['daily'].keys())
    new_days = determine_new_days(item_id, list_of_days, session_lock)
    updated_dict = dict((key, value) for key, value in json_response['daily'].items() if int(key) in new_days)
    list_of_prices = [Price(item_id=item_id, runescape_time=int(key), price=value) for key, value in updated_dict]
    add_all_to_database(list_of_prices, session_lock)


def get_all_historic_prices(session_lock: multiprocessing.Lock, runescape_lock: multiprocessing.Lock) -> list:
    return get_historic_prices(get_ids_in_database(session_lock), session_lock, runescape_lock)


if __name__ == '__main__':
    processes = get_all_historic_prices(multiprocessing.Lock(), multiprocessing.Lock())
