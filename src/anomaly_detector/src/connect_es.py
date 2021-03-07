import datetime
import sys
from urllib3.exceptions import LocationValueError

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
import json
from typing import Dict, List, Tuple

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
        
    def get_timestamp_metrics_sequence(self, target_web_page_url: str) -> List:
        """Get page speed metrics from Elasticsearch"""
        index_name = f'{Config.INDEX_PREFIX}-*'
        search_query = self._create_search_query(target_web_page_url)
        try:
            result = self._client.search(index=index_name, body=search_query)
        except ConnectionError:
            raise GetTimestampMetricsSequenceError
        else:
            # Order of these sequence is desc ([latest, ..., oldest])
            timestamp_metrics_sequence = []
            for record in result['aggregations']['histogram']['buckets']:
                timestamp = datetime.datetime.fromtimestamp(record['key'] // 1000)
                metrics = record['metrics_average']['value']
                timestamp_metrics_sequence.append((timestamp, metrics))
            return timestamp_metrics_sequence
        
    def close(self) -> None:
        """Close the connection with Elasticsearch"""
        try:
            self._client.close()
            logger.info('Successfully connection closed')
        except ConnectionError:
            raise ConnectionCloseError
        
    def _create_search_query(self, target_web_page_url: str) -> Dict:
        """Create search query to get metrics from Elasticsearch"""
        with open(Config.SEARCH_QUERY_FILE) as file:
            search_query = json.load(file)

        search_query['query']['bool']['filter'][0]['term']['target_url'] = target_web_page_url
        search_query['query']['bool']['filter'][1]['term']['platform'] = Config.PLATFORM
        search_query['aggs']['histogram']['aggs']['metrics_average']['avg']['field'] = Config.ALERT_TARGET_METRICS
        search_query['aggs']['histogram']['aggs']['timestamp_sort']['bucket_sort']['size'] = Config.METRICS_SEQUENCE_LENGTH
        
        logger.debug('----------------------------Search Query----------------------------')
        logger.debug(search_query)
        logger.debug('--------------------------------------------------------------------')
        
        return search_query
    
    