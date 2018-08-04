import multiprocessing
import numpy as np

from database.in_database import get_days_for_item


def get_points_data_set(item_id: int, data_range: int, session_lock: multiprocessing.Lock) -> list:
    points = [(x[0]//86400000, x[1]) for x in get_days_for_item(item_id, session_lock)]
    return [get_points_for_day(points, point, data_range)[0] for point in points if
            any(point[0] < inner_point[0] <= point[0] + data_range for inner_point in points)
            and len(get_points_for_day(points, point, data_range)) == 7]


def get_x_points_data_set(data_set: list) -> np.array:
    data_points_size = len(data_set[0])
    data_set_size = len(data_set)
    training_data_set = data_set[:round(data_set_size * .8)]
    test_data_set = data_set[round(data_set_size * .8):]
    return [np.array([data[:data_points_size-1] for data in training_data_set]),
            np.array([data[:data_points_size-1] for data in test_data_set])]


def get_y_points_data_set(data_set: list) -> np.array:
    data_points_size = len(data_set[0])
    data_set_size = len(data_set)
    training_data_set = data_set[:round(data_set_size * .8)]
    test_data_set = data_set[round(data_set_size * .8):]
    return [np.array([data[data_points_size - 1:][0] for data in training_data_set]),
            np.array([data[data_points_size - 1:][0] for data in test_data_set])]


def get_points_for_day(points: list, end_point: tuple, data_range: int) -> list:
    return [x for x in points if end_point[0] < x[0] <= end_point[0] + data_range]


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    a_list = get_points_data_set(554, 7, lock)
    print(a_list[0])
    print(get_x_points_data_set(a_list)[0])
    print(get_y_points_data_set(a_list)[0])
