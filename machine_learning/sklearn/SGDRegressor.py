import multiprocessing
from sklearn import linear_model

from predict_next_day import get_points_data_set, get_x_points_data_set, get_y_points_data_set

if __name__ == '__main__':
    data_set = get_points_data_set(554, 14, multiprocessing.Lock())
    # print(data_set)
    sgd_regressor = linear_model.SGDRegressor(loss="epsilon_insensitive", tol=.3, eta0=.0001, power_t=.15)
    x_points_data_set = get_x_points_data_set(data_set)
    y_points_data_set = get_y_points_data_set(data_set)
    # print("x points: {}".format(x_points_data_set))
    # print("y points: {}".format(y_points_data_set))
    training_x_points = x_points_data_set[0]
    testing_x_points = x_points_data_set[1]
    training_y_points = y_points_data_set[0]
    testing_y_points = y_points_data_set[1]
    # print(training_x_points)
    # print(training_y_points)
    sgd_regressor.fit(training_x_points, training_y_points)
    print("Predicting: {}".format([int(round(x)) for x in sgd_regressor.predict(testing_x_points)]))
    # print("Tried: {}".format(testing_x_points))
    print("Expected:   {}".format([x for x in testing_y_points]))
    print(sgd_regressor.score(testing_x_points, testing_y_points))
