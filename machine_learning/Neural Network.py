import multiprocessing

from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score, mean_squared_error

from get_data_sets import get_x_points_data_set, get_y_points_data_set, get_points_data_set

'''
Notes: lbfgs solver seems to be doing the best overall especially with larger size of input
'''


if __name__ == '__main__':
    for i in range(1, 6):
        print("Iteration: {}".format(i))
        data_set = get_points_data_set(554, i, multiprocessing.Lock())
        # print(data_set)
        sgd_regressor = MLPRegressor(solver='lbfgs', learning_rate='adaptive', hidden_layer_sizes=(7,))
        x_points_data_set = get_x_points_data_set(data_set)
        y_points_data_set = get_y_points_data_set(data_set)
        # print("x points: {}".format(x_points_data_set))
        # print("y points: {}".format(y_points_data_set))
        training_x_points = x_points_data_set[0]
        testing_x_points = x_points_data_set[1]
        training_y_points = y_points_data_set[0]
        testing_y_points = y_points_data_set[1]
        sgd_regressor.fit(training_x_points, training_y_points)
        predicted = [int(round(x)) for x in sgd_regressor.predict(testing_x_points)]
        true = [x for x in testing_y_points]
        print("Previous Day: {}".format([x[0] for x in testing_x_points]))
        print("Predicting:   {}".format(predicted))
        print("True:         {}".format(true))
        # print("Score: {}".format(sgd_regressor.score(testing_x_points, testing_y_points)))
        print("Mean squared error: {}".format(mean_squared_error(true, predicted)))
        print("R2: {}".format(r2_score(true, predicted)))
        print()
