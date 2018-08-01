import sqlite3

import requests
import multiprocessing
import json
import time

import sqlalchemy

import py_logging
from database_services.database.in_database import get_ids_in_database
from database_services.database_objects.price import Price
from database_services.database_objects.item import Item
from get_processors import get_number_of_processors_running


def get_historic_prices(item_ids: list, session_lock: multiprocessing.Lock, runescape_lock: multiprocessing.Lock) -> list:
    processes = []
    for item_id in reversed(item_ids):
        while get_number_of_processors_running(processes) >= multiprocessing.cpu_count():
            time.sleep(1)
        process = multiprocessing.Process(target=get_historic_prices_one_id, args=(item_id, session_lock, runescape_lock))
        process.start()
        processes.append(process)
        print("Started process to get the historical data for {}".format(item_id))
    return processes


def get_historic_prices_one_id(item_id: int, session_lock: multiprocessing.Lock, runescape_lock: multiprocessing.Lock):
    with runescape_lock:
        print("Got lock")
        response = requests.get("http://services.runescape.com/m=itemdb_rs/api/graph/{}.json".format(item_id))
        if "You've made too many requests recently." in response.text:
            print("Too many requests")
            time.sleep(30)
            json_response = requests.get("http://services.runescape.com/m=itemdb_rs/api/graph/{}.json".format(item_id)).json()
        else:
            json_response = response.json()
        # time.sleep(5)
    print("Starting to parse the data for {}".format(item_id))
    for key, value in json_response['daily'].items():
        try:
            Price(item_id=item_id, runescape_time=int(key), price=value).add_to_database(session_lock)
        except (sqlalchemy.exc.IntegrityError, sqlite3.IntegrityError):
            pass
            # print("Failed to update price for {} on runescape day {}".format(item_id, key))


def get_all_historic_prices(session_lock: multiprocessing.Lock, runescape_lock: multiprocessing.Lock) -> list:
    return get_historic_prices(get_ids_in_database(session_lock), session_lock, runescape_lock)


if __name__ == '__main__':
    processes = get_all_historic_prices(multiprocessing.Lock(), multiprocessing.Lock())
    num_proc_running = get_number_of_processors_running(processes)
    while num_proc_running > 1:
        print(num_proc_running)
        num_proc_running = get_number_of_processors_running(processes)
