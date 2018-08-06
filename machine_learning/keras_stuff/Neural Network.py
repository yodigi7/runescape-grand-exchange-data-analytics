import multiprocessing
import random

import time
from keras.wrappers.scikit_learn import KerasRegressor
from keras.layers import Dense
from keras.models import Sequential

import predict_min_max_data_range
import predict_next_day


# TODO: Wait for tensorflow to be updated to support Python 3.7


def baseline_model(input_size: int=7, output_size: int=1):
    model = Sequential()
    model.add(Dense(input_size, input_dim=input_size, kernel_initializer='normal', activation='relu'))
    model.add(Dense(input_size//2, kernel_initializer='normal', activation='relu'))
    model.add(Dense(output_size, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


if __name__ == '__main__':
    data_set = predict_next_day.get_points_data_set(554, i, multiprocessing.Lock())
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
    estimator = baseline_model.fit(training_x_points, training_y_points, epochs=100, batch_size=5)
