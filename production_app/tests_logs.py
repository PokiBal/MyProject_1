# import logging

# class BaseClass:
#     def log_conf(self):
#         logger = logging.getLogger(__name__)
#         fileHandler = logging.FileHandler("logfile.log")
#         formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(message)s :")
#         fileHandler.setFormatter(formatter)
#         logger.addHandler(fileHandler)
#         logger.setLevel(logging.DEBUG)
#         return logger
    
from logfile import logger

def test_logging():
    logger.info('Test logging message')
    with open('db.log', 'rt') as log:
        assert 'Test logging message' in log.read()
