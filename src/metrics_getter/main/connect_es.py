import datetime
import json
import time
from typing import Dict
from urllib3.exceptions import LocationValueError

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

from config import Config
from exceptions import *
from logger import logger


class ElasticsearchConnector:
    
    def __init__(self):
        """Get Elasticsearch client"""
        try:
            self.__client = Elasticsearch(Config.ELASTICSEARCH_URL)
        except LocationValueError:
            raise IncorrectElasticsearchURLError
        
    def create_index_template(self) -> None:
        """Create index template of Elasticsearch if not exists"""
        try:
            index_template_exists = self.__client.indices.exists_index_template(name=Config.INDEX_TEMPLATE_NAME)
        except ConnectionError:
            raise IndexPatternConfirmError
        
        if index_template_exists:
            return
        
        with open(Config.INDEX_TEMPLATE_FILE) as file:
            index_template = json.load(file)
            
        index_template['index_patterns'].append(f'{Config.INDEX_PREFIX}-*')
        try:
            self.__client.indices.put_index_template(name=Config.INDEX_TEMPLATE_NAME, body=index_template, master_timeout=3)
            logger.info('Index Patterns successfully processed')
        except ConnectionError:
            raise IndexPatternCreationError

            
    def insert(self, metrics: Dict) -> None:
        """Insert obtained metrics to Elasticsearch"""
        epoch_ms = str(int(time.time() * 1000))
        today = datetime.date.today()
        
        index_name = f'{Config.INDEX_PREFIX}-{today}'
        body = metrics.copy()
        body['@timestamp'] = epoch_ms
        body['target_url'] = Config.TARGET_WEB_PAGE_URI
        body['platform'] = Config.PLATFORM
        
        try:
            self.__client.index(index=index_name, body=body, refresh='wait_for')
            logger.info('Metrics successfully inserted to Elasticsearch')
        except ConnectionError:
            raise MetricsInsertError

    def close(self) -> None:
        """Close the connection with Elasticsearch"""
        try:
            self.__client.close()
            logger.info('Successfully connection closed')
        except ConnectionError:
            raise ConnectionCloseError