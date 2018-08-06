import multiprocessing
import numpy as np

from database.in_database import get_days_for_item


def get_x_points_data_set(data_set: list) -> list:
    data_set_size = len(data_set)
    training_data_set = data_set[:round(data_set_size * .8)]
    test_data_set = data_set[round(data_set_size * .8):]
    training_data_set_holder = training_data_set[:]
    testing_data_set_holder = test_data_set[:]
    return [[data[1:] for data in training_data_set_holder],
            [data[1:] for data in testing_data_set_holder]]


def get_points_data_set(item_id: int, data_range: int, session_lock: multiprocessing.Lock) -> list:
    points = [(x[0]//86400000, x[1]) for x in get_days_for_item(item_id, session_lock)]
    return [get_points_for_day(points, point, data_range) for point in points if
            any(point[0] < inner_point[0] <= point[0] + data_range for inner_point in points)
            and len(get_points_for_day(points, point, data_range)) == data_range + 1]


def get_y_points_data_set(data_set: list) -> list:
    data_set_size = len(data_set)
    training_data_set = data_set[:round(data_set_size * .8)]
    test_data_set = data_set[round(data_set_size * .8):]
    return [np.array([data[0] for data in training_data_set]),
            np.array([data[0] for data in test_data_set])]


def get_points_for_day(points: list, end_point: tuple, data_range: int) -> list:
    return [x[1] for x in points if end_point[0] <= x[0] <= end_point[0] + data_range]


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    points = [(x[0] // 86400000, x[1]) for x in get_days_for_item(554, lock)]
    data_set = get_points_data_set(554, 7, lock)
    print(points)
    print(get_points_for_day(points, (1520726400000 // 86400000, 123), 7))
    print(data_set)
    x_points = get_x_points_data_set(data_set)
    y_points = get_y_points_data_set(data_set)
    print(x_points[0])
    print(y_points[0])
