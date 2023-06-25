import logging
import os
from datetime import datetime

Log_File= f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


logs_path=os.path.join(os.getcwd(),"logs",Log_File)
os.makedirs(logs_path,exist_ok=True)
Log_File_should_be_Stored_at_path = os.path.join(logs_path,Log_File)

logging.basicConfig(
    filename=Log_File_should_be_Stored_at_path,
    format="[%(asctime)s] %(lineno)d -%(name)s -%(levelname)s-%(message)s",
    level=logging.INFO

)