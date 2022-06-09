from keras.models import Sequential
from keras.layers import Dense,LSTM
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import math
import pandas as pd


def get_prediction(df):
    data = df.filter(['Close'])
    dataSet = data.values
    training_data_len = math.ceil(len(dataSet) * .8)
    scaler = MinMaxScaler(feature_range = (0,1))
    scaled_data = scaler.fit_transform(dataSet)
    train_data = scaled_data[0:training_data_len,:]

    x_train = []
    y_train = []

    for i in range(60,len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i,0])
        if i<=61:
            print(x_train)
            print(y_train)
            print()

    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_train.shape

    model = Sequential()
    model.add(LSTM(50, return_sequences = True, input_shape = (x_train.shape[1],1)))
    model.add(LSTM(50, return_sequences = False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile(optimizer = 'adam' , loss = 'mean_squared_error')

    model.fit(x_train, y_train, batch_size = 1, epochs = 1)

    test_data = scaled_data[training_data_len-60: , :]

    x_test = []
    y_test = dataSet[training_data_len: , :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])

    x_test = np.array(x_test)

    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    rmse = np.sqrt(np.mean(predictions- y_test)**2)
    rmse

    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions
    
    # df0 = {}
    # df0['Train'] = train['Close']
    # df0['Test'] = valid['Close']
    # df0['Predictions'] = valid['Predictions'] 
    # df0 = pd.DataFrame(df0)

    return valid