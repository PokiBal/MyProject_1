# with open("logfile.log", "r") as f:
#     last_line = f.readlines()[-1]
#     entry = last_line.strip().split(":")
#     timestamp = entry[0] + ":" + entry[1]
#     message = entry[4].strip().replace('"', '\\"')

# print(f"{timestamp}, {message}")

import logging

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# For example, setup logger with name 'db'
logger = setup_logger('db', 'db.log')
logger.info('This is a log message')
