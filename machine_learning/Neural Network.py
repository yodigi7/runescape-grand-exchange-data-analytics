import multiprocessing
import random

import time
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score, mean_squared_error

import predict_min_max_data_range
import predict_next_day

'''
Notes: lbfgs solver seems to be doing the best overall especially with larger size of input
'''


def test_neural_network_one_day():
    for i in range(1, 15):
        print("Iteration: {}".format(i))
        data_set = predict_next_day.get_points_data_set(554, i, multiprocessing.Lock())
        mlpregressor = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(i*3,))
        x_points_data_set = predict_next_day.get_x_points_data_set(data_set)
        y_points_data_set = predict_next_day.get_y_points_data_set(data_set)
        holder = list(zip(x_points_data_set, y_points_data_set))
        random.shuffle(holder)
        x_points_data_set, y_points_data_set = zip(*holder)
        time.sleep(1)
        training_x_points = x_points_data_set[0]
        testing_x_points = x_points_data_set[1]
        training_y_points = y_points_data_set[0]
        testing_y_points = y_points_data_set[1]
        mlpregressor.fit(training_x_points, training_y_points)
        predicted = [int(round(x)) for x in mlpregressor.predict(testing_x_points)]
        true = [x for x in testing_y_points]
        print("Previous Day: {}".format([x[0] for x in testing_x_points]))
        print("Predicting:   {}".format(predicted))
        print("True:         {}".format(true))
        print("Mean squared error: {}".format(mean_squared_error(true, predicted)))
        print("R2: {}".format(r2_score(true, predicted)))
        print()


def test_neural_network_min_max(item_id: int, input_size: int, output_size: int, hidden_layers: list) -> None:
    data_set = predict_min_max_data_range.get_points(item_id, input_size, output_size, multiprocessing.Lock())
    mlpregressor = MLPRegressor(solver='lbfgs', hidden_layer_sizes=hidden_layers)
    x_points_data_set = predict_min_max_data_range.get_x_points_data_set(data_set)
    y_points_data_set = predict_min_max_data_range.get_y_points_data_set(data_set)
    holder = list(zip(x_points_data_set, y_points_data_set))
    random.shuffle(holder)
    x_points_data_set, y_points_data_set = zip(*holder)
    x_points_data_set = list(x_points_data_set)
    y_points_data_set = list(y_points_data_set)
    x_points_data_set.sort(key=lambda x: -len(x))
    y_points_data_set.sort(key=lambda y: -len(y))
    time.sleep(1)
    training_x_points = x_points_data_set[0]
    testing_x_points = x_points_data_set[1]
    training_y_points = y_points_data_set[0]
    testing_y_points = y_points_data_set[1]
    print("Number of training points: {}".format(len(training_x_points)))
    print("Number of testing points:  {}".format(len(testing_x_points)))
    mlpregressor.fit(training_x_points, training_y_points)
    predicted = [[int(round(x)) for x in num] for num in mlpregressor.predict(testing_x_points)]
    true = [x for x in testing_y_points]
    print("Predicting:   {}".format(predicted))
    print("True:         {}".format(true))
    print("Mean squared error: {}".format(mean_squared_error(true, predicted)))
    print("R2: {}".format(r2_score(true, predicted)))
    print()


if __name__ == '__main__':
    test_neural_network_min_max(556, 7, 3, [7])
