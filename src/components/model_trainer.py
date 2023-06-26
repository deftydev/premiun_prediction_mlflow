import numpy as np
import pandas as pd
import argparse
import mlflow
import mlflow.sklearn

from sklearn.linear_model import LinearRegression, Ridge,Lasso,ElasticNet
from src.exception import CustomException
from src.logger import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV 
from sklearn import tree
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.utils import save_object
from src.utils import evaluate_models

from dataclasses import dataclass
import sys
import os


@dataclass
class ModelTrainerConfig:
    model_file_path= os.path.join("artifacts","model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config= ModelTrainerConfig()

    def model_building(self,train_arr,test_arr,preprocessor_obj_file,n_estimators,max_depth,min_samples_leaf):

        try:
            logging.info('Splitting Dependent and Independent variables from train and test data')
            X_train = train_arr[:,:-1]
            Y_train = train_arr[:,-1]
            X_test  = test_arr[:,:-1]
            Y_test  = test_arr[:,-1]
            with mlflow.start_run():
                Random_forest=RandomForestRegressor(criterion= 'friedman_mse',n_estimators=25,max_depth=6,min_samples_leaf=8)

                obj= Random_forest.fit(X_train,Y_train)
                y_pred= obj.predict(X_test)
                mae,rmse,r2 = evaluate_models(Y_test,y_pred)

                logging.info(f'mae : {mae}')
                logging.info(f'rmse : {rmse}')
                logging.info(f'r2 : {r2}')

                best_model= "Random_forest"

                mlflow.log_param("n_estimators",n_estimators)
                mlflow.log_param("max_depth", max_depth)
                mlflow.log_param("min_samples_leaf",min_samples_leaf)
                mlflow.log_metric("R2",r2)
                
                logging.info('\n====================================================================================\n')
                logging.info(f'Best Model Found , Model Name : {best_model} , R2 Score : {r2}')
                #mlflow model logging
                mlflow.sklearn.log_model(Random_forest,"randomforestmodel")
                save_object(
                    file_path=self.model_trainer_config.model_file_path,
                    obj= Random_forest
                    )


        except Exception as e:
            logging.info("model creation is having some error")
            raise CustomException(e,sys)
        
if __name__ == '__main__':
    args=argparse.ArgumentParser()
    args.add_argument("--n_estimators", "-n", default=25, type=int)
    args.add_argument("--max_depth", "-m", default=6, type=int)
    args.add_argument("--min_samples_leaf", "-s", default=8, type=int)
    parse_args=args.parse_args()
    try:
        obj= DataIngestion()
        t1,t2= obj.initiate_data_ingestion()
        obj1= DataTransformation()
        train,test,pre= obj1.initaite_data_transformation(t1,t2)
        obj2= ModelTrainer()
        obj2.model_building(train,test,pre,n_estimators=parse_args.n_estimators,max_depth=parse_args.max_depth,min_samples_leaf=parse_args.min_samples_leaf)
        
    except Exception as e:
        logging.info("Model training is having error")
        raise CustomException(e,sys)