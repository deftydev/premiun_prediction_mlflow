import os
import sys
import pickle
import numpy as np 
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from src.exception import CustomException
from src.logger import logging

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    

def evaluate_model(y_test,y_pred):

    mae= mean_absolute_error(y_test,y_pred)
    rmse= np.sqrt(mean_squared_error(y_test,y_pred))

    r2= r2_score(y_test,y_pred)

    return mae,rmse,r2

def evaluate_models(y_test,y_pred):

    mae= mean_absolute_error(y_test,y_pred)
    rmse= np.sqrt(mean_squared_error(y_test,y_pred))

    r2= r2_score(y_test,y_pred)

    return mae,rmse,r2


def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.info('Exception Occured in load_object function utils')
        raise CustomException(e,sys)