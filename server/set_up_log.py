import logging
from pythonjsonlogger import jsonlogger

def log_setup(level = logging.INFO):
    root_logger= logging.getLogger()
    root_logger.setLevel(level)
    handler = logging.FileHandler('error.log', 'a', 'utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))
    root_logger.addHandler(handler)

def json_log_setup(level = logging.DEBUG):
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(level)
    logHandler = logging.FileHandler('error_json.log', 'a', 'utf-8')
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)