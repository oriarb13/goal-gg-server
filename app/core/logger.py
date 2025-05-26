import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
        handlers=[ #where the logs 
            logging.StreamHandler(sys.stdout),  #for the console
            logging.FileHandler('app.log', encoding='utf-8')  #for log file
        ]
    )

setup_logging() 

def get_logger(name):
    return logging.getLogger(name)