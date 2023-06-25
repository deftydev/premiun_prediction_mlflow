import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge,Lasso,ElasticNet
from src.exception import CustomException
from src.logger import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV 
from sklearn import tree

from src.utils import save_object
from src.utils import evaluate_model

from dataclasses import dataclass
import sys
import os


@dataclass
class ModelTrainerConfig:
    model_file_path= os.path.join("artifacts","model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config= ModelTrainerConfig()

    def model_building(self,train_arr,test_arr,preprocessor_obj_file):

        try:
            logging.info('Splitting Dependent and Independent variables from train and test data')
            X_train = train_arr[:,:-1]
            Y_train = train_arr[:,-1]
            X_test  = test_arr[:,:-1]
            Y_test  = test_arr[:,-1]
            models={
                'Random_forest':RandomForestRegressor(criterion= 'friedman_mse',max_depth=6,min_samples_leaf=8,n_estimators=25)
                }
            
            report = evaluate_model(models,X_train,Y_train,X_test,Y_test)
            logging.info(f'Model Report : {report}')
            print(report.keys())
            print(report.values())
            best_model_score= max(sorted(report.values()))
            print(best_model_score)

            best_model_name= list(report.keys())[list(report.values()).index(best_model_score)]
            best_model= models[best_model_name]

            
            print(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')
            print('\n====================================================================================\n')
            logging.info(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')


            save_object(
                file_path=self.model_trainer_config.model_file_path,
                obj= best_model
            )


        except Exception as e:
            logging.info("model creation is having some error")
            raise CustomException(e,sys)