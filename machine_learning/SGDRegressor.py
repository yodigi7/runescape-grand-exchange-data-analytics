import multiprocessing
import numpy as np
from sklearn import linear_model

from get_data_sets import get_points_data_set, get_x_points_data_set, get_y_points_data_set

if __name__ == '__main__':
    data_set = get_points_data_set(1128, 7, multiprocessing.Lock())
    print(data_set)
    sgd_regressor = linear_model.SGDRegressor()
    training_x_points = get_x_points_data_set(data_set)[0]
    testing_x_points = get_x_points_data_set(data_set)[1]
    training_y_points = get_y_points_data_set(data_set)[0]
    testing_y_points = get_y_points_data_set(data_set)[1]
    print(training_x_points)
    print(training_y_points)
    sgd_regressor.fit(training_x_points, training_y_points)
    print(sgd_regressor.score(training_x_points, training_y_points))
