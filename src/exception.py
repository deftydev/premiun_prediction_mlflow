import sys
import os

from src.logger import logging

def get_error_detail(error_messages,error_detail:sys):
    _,_,exc_tb= error_detail.exc_info()
    file_name= exc_tb.tb_frame.f_code.co_filename

    error_message= "Error occured in file named {0}, at line number {1} - error {2}".format(file_name, exc_tb.tb_lineno,str(error_messages))

    return error_message



class CustomException(Exception):

    def __init__(self,error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message= get_error_detail(error_message,error_detail=error_detail)


    def __str__(self) :
        return self.error_message
    
if __name__=="__main__":

    logging.info('Logging has started')

    try:
        a=0/0
    except Exception as e:
        logging.info('Some error occured')
        raise CustomException(e,sys)