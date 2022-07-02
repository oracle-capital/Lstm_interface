import numpy as np    
from scipy.stats import norm 


def get_prediction(data):
    days_to_test = 100      
    days_to_predict = 1    
    simulations = 1000
    daily_return = np.log(1 + data.pct_change())
    average_daily_return = daily_return.mean()
    variance = daily_return.var()
    drift = average_daily_return - (variance/2)
    standard_deviation = daily_return.std()
    predictions = np.zeros(days_to_test+days_to_predict)
    predictions[0] = data[-days_to_test]
    pred_collection = np.ndarray(shape=(simulations,days_to_test+days_to_predict))
    for j in range(0,simulations):
        for i in range(1,days_to_test+days_to_predict):
            random_value = standard_deviation * norm.ppf(np.random.rand())
            predictions[i] = predictions[i-1] * np.exp(drift + random_value)
        pred_collection[j] = predictions


    ############################################################################
    differences = np.array([])
    for k in range(0,simulations):
        difference_arrays = np.subtract(data.values[-100:],pred_collection[k][:-1])
        difference_values = np.sum(np.abs(difference_arrays))
        differences = np.append(differences,difference_values)
        
    best_fit = np.argmin(differences)
    future_price = pred_collection[best_fit][-1]

    return predictions, future_price