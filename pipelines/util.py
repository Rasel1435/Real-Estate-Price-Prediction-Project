import json
import pickle
import os
import numpy as np
import warnings

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location,sqft,bhk,bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)

def load_saved_artifacts(): 
    print("Loading saved artifacts...")

    global __data_columns
    global __locations
    global __model

    try:
        # Get the directory path of util.py
        current_dir = os.path.dirname(__file__)

        # Path to columns.json
        columns_json_path = os.path.join(current_dir,'..', 'artifacts', 'columns.json')
        with open(columns_json_path, 'r') as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

        # Suppress the warning
        warnings.filterwarnings("ignore", category=UserWarning)
        # Path to model.pickle
        model_pickle_path = os.path.join(current_dir,'..', 'artifacts', 'model.pickle')
        global __model
        with open(model_pickle_path, 'rb') as f:
            __model = pickle.load(f)

        print("Loading saved artifacts... Done")
    except Exception as e:
        print("Error loading saved artifacts:", e)
        
def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2)) # other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))  # other location