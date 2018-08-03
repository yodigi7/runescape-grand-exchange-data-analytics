import os

import multiprocessing
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

import py_logging
from database.in_database import get_days_for_item

from database_services.session_controller import shared_session
from database_services.database_objects.item import Item
from database_services.database_objects.price import Price
from get_config import get_config


def get_points_data_set(item_id: int, data_range: int, session_lock: multiprocessing.Lock) -> list:
    points = [(x[0]//86400000, x[1]) for x in get_days_for_item(item_id, session_lock)]
    return [get_points_for_day(points, point, data_range) for point in points if
            any(point[0] < inner_point[0] <= point[0] + data_range for inner_point in points)
            and len(get_points_for_day(points, point, data_range)) == 7]


def get_points_for_day(points: list, end_point: tuple, data_range: int) -> list:
    return [x for x in points if end_point[0] < x[0] <= end_point[0] + data_range]


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    print([(x[0]//86400000, x[1]) for x in get_days_for_item(554, lock)])
    a_list = get_points_data_set(554, 7, lock)
    for data in a_list:
        if not len(data) == 7:
            print(data)
