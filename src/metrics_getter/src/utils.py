from typing import List

from config import Config
from logger import logger


def show_config_contents() -> None:
    logger.debug('----------------------------Config----------------------------')
    for key, value in Config.__dict__.items():
        logger.debug(f'{key}: {value}')
    logger.debug('--------------------------------------------------------------')
    
    
def get_web_page_url_list() -> List:
    web_page_url_str = Config.TARGET_WEB_PAGE_URI.replace(' ', '').replace('\n', '').replace('\t', '')
    web_page_url_list = web_page_url_str.split(',')
    return web_page_url_list