import logging

from config import Config


def get_logger(name=None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    
    sh = logging.StreamHandler()
    sh.setLevel(Config.LOG_LEVEL)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    
    return logger