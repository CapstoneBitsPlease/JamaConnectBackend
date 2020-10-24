import logging

def log_setup(level = logging.DEBUG):
    root_logger= logging.getLogger()
    root_logger.setLevel(level)
    handler = logging.FileHandler('error.log', 'a', 'utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))
    root_logger.addHandler(handler)