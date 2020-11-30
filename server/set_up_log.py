import logging
from pythonjsonlogger import jsonlogger

def json_log_setup(level = logging.INFO):
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(level)
    logHandler = logging.FileHandler('error_json.log', 'a', 'utf-8')
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)