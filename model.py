import warnings

warnings.simplefilter('ignore')
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle
import os

# %matplotlib inline
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

variables = ["FairMarketRent_2BR", '0-1 BedroomUnits', 'TwoBedroomUnits', 'ThreePlusBedroomUnits']


# Read the csv file into a pandas DataFrame
def model():
    data_og = pd.read_excel('website/db/Active and Inconclusive Properties GA.xlsx')

    for variable in variables:
        data = data_og[["Latitude", "Longitude", variable]]

        data.dropna(axis=1, how='all', inplace=True)
        data.dropna(inplace=True)

        X = data[["Latitude", "Longitude"]]
        y = data[variable].values.reshape(-1, 1)
        print(X.shape, y.shape)

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

        # Plot the results

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        # Calculate the absolute errors
        errors = abs(predictions - y_test)

        # Print out the mean absolute error (mae)
        print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')

        # predictions = y_new_inverse
        MSE = mean_squared_error(y_test, predictions)
        RMSE = np.sqrt(MSE)
        print(variable)
        print(f"MSE: {MSE}, RMSE: {RMSE}")

        filename = 'website/db/finalized_model_' + variable + '.sav'
        pickle.dump(model, open(filename, 'wb'))

# model()

def run_fmr(lat,lon):
    variable = 'FairMarketRent_2BR'
    print(os.getcwd())
    try:
        filename = '../website/db/finalized_model_' + variable + '.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
    except:
        filename = 'website/db/finalized_model_' + variable + '.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
    data = pd.DataFrame({'Latitude': [lat], 'Longitude': [lon]})
    predictions = loaded_model.predict(data)
    print(predictions[0])
    return predictions[0]


# run_by_model(33.74632,-84.28033,'FairMarketRent_2BR')

def run_beds(lat,lon):
    variables_beds = ['0-1 BedroomUnits', 'TwoBedroomUnits', 'ThreePlusBedroomUnits']
    data_beds = pd.DataFrame({'Size': [], 'Beds': []})
    for variable in variables_beds:
        try:
            filename = '../website/db/finalized_model_' + variable + '.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
        except:
            filename = 'website/db/finalized_model_' + variable + '.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
        data = pd.DataFrame({'Latitude': [lat], 'Longitude': [lon]})
        predictions = loaded_model.predict(data)

        data_beds = data_beds.append(pd.DataFrame({'Size': [variable], 'Beds': [predictions[0]]}))

        print(predictions[0])
    data_beds['Beds'] = (data_beds['Beds']*100 / data_beds['Beds'].sum()).astype(int).astype(str) + '%'
    # print(data_beds)
    data_beds = list(data_beds['Beds'])
    return data_beds


# run_beds(33.74632,-84.28033)