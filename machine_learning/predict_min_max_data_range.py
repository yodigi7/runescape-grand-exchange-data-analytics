import multiprocessing

from predict_next_day import get_points_data_set


def get_points(item_id: int, input_data_range: int, output_data_range: int, session_lock: multiprocessing.Lock) -> list:
    return [data_point[:input_data_range] +
            list((min(data_point[input_data_range:]),
                  max(data_point[input_data_range:])))
            for data_point in (get_points_data_set(item_id, input_data_range + output_data_range - 1, session_lock))]


def get_x_points_data_set(data_set: list) -> list:
    return [[data[:len(data_set[0]) - 2] for data in (data_set[:round(len(data_set) * .8)][:])],
            [data[:len(data_set[0]) - 2] for data in (data_set[round(len(data_set) * .8):][:])]]


def get_y_points_data_set(data_set: list) -> list:
    return [[data[len(data_set[0]) - 2:] for data in (data_set[:round(len(data_set) * .8)][:])],
            [data[len(data_set[0]) - 2:] for data in (data_set[round(len(data_set) * .8):][:])]]


if __name__ == '__main__':
    points = get_points(554, 7, 7, multiprocessing.Lock())
    print(points)
    print(get_x_points_data_set(points))
    print(get_y_points_data_set(points))
