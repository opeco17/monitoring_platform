import datetime
import json
import time
from typing import Dict, List, Tuple
from urllib3.exceptions import LocationValueError

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
from elasticsearch.helpers import bulk

from config import Config
from exceptions import *
from logger import logger


class ElasticsearchConnector:
    
    def __init__(self):
        """Set Elasticsearch client"""
        try:
            self._client = Elasticsearch(Config.ELASTICSEARCH_URL)
        except LocationValueError:
            raise IncorrectElasticsearchURLError
        
    def create_index_template(self) -> None:
        """Create index template of Elasticsearch if not exists"""
        try:
            index_template_exists = self._client.indices.exists_index_template(name=Config.INDEX_TEMPLATE_NAME)
        except ConnectionError:
            raise IndexPatternConfirmError
        
        if index_template_exists:
            return
        
        with open(Config.INDEX_TEMPLATE_FILE) as file:
            index_template = json.load(file)
            
        index_template['index_patterns'].append(f'{Config.INDEX_PREFIX}-*')
        try:
            self._client.indices.put_index_template(name=Config.INDEX_TEMPLATE_NAME, body=index_template, master_timeout=3)
            logger.info('Index Patterns successfully processed')
        except ConnectionError:
            raise IndexPatternCreationError

            
    def insert(self, metrics: Dict) -> None:
        """Insert obtained metrics to Elasticsearch"""
        index_name, body = self._prepare_data_for_insert(metrics)
        try:
            self._client.index(index=index_name, body=body, refresh='wait_for')
            logger.info('Metrics successfully inserted to Elasticsearch')
        except ConnectionError:
            raise MetricsInsertError
        
    def bulk_insert(self, metrics_list: List) -> None:
        """Bulk insert obtained metrics to Elasticsearch"""
        try:
            bulk(self._client, self._prepare_data_for_bulk_insert(metrics_list))
            logger.info('Metrics successfully bulk inserted to Elasticsearch')
        except ConnectionError:
            raise MetricsInsertError
        
    def close(self) -> None:
        """Close the connection with Elasticsearch"""
        try:
            self._client.close()
            logger.info('Successfully connection closed')
        except ConnectionError:
            raise ConnectionCloseError
        
    def _prepare_data_for_insert(self, metrics: Dict) -> Tuple[str, Dict]:
        epoch_ms = str(int(time.time() * 1000))
        today = datetime.date.today()
        index_name = f'{Config.INDEX_PREFIX}-{today}'
        body = metrics.copy()
        body['@timestamp'] = epoch_ms
        return index_name, body
    
    def _prepare_data_for_bulk_insert(self, metrics_list: List) -> Dict:
        for metrics in metrics_list:
            index_name, body = self._prepare_data_for_insert(metrics)
            bulk_body = body.copy()
            bulk_body['_index'] = index_name
            yield bulk_body