import datetime
import json
import sys
import time
from typing import Dict, List, Tuple

from elasticsearch import Elasticsearch
import requests
from requests.models import Response
from requests.exceptions import HTTPError
from retry import retry

from config import Config
from logger import get_logger


logger = get_logger()


def create_search_query() -> Dict:
    """Create search query to get metrics from Elasticsearch"""
    with open(Config.SEARCH_QUERY_FILE) as search_query_file:
        search_query = json.load(search_query_file)
        
    search_query['size'] = int(Config.METRICS_SEQUENCE_LENGTH)
    search_query['_source'].append(Config.ALERT_TARGET_METRICS)
    search_query['query']['bool']['filter'][0]['term']['target_url'] = Config.TARGET_WEB_PAGE_URI
    search_query['query']['bool']['filter'][1]['term']['platform'] = Config.PLATFORM
    
    logger.debug('----------------------------Search Query----------------------------')
    logger.debug(search_query)
    logger.debug('--------------------------------------------------------------------')
    
    return search_query


def check_obtained_records(metrics_sequence: List, timestamp_sequence:List) -> None:
    """Check whether the sequence is obtained correctly"""
    pass


def search_metrics_sequence(elasticsearch: Elasticsearch) -> Tuple:
    """Get page speed metrics from Elasticsearch"""
    index_name = f'{Config.INDEX_PREFIX}-*'
    search_query = create_search_query()
    result = elasticsearch.search(index=index_name, body=search_query)
    if not result['_shards']['failed'] == 0:
        logger.info('Failed to get metrics from Elasticsearch.')
        sys.exit(1)
        
    logger.info('Get metrics from Elasticsearch successfully.')
    
    metrics_sequence = [record['_source'][Config.ALERT_TARGET_METRICS] for record in result['hits']['hits']]
    timestamp_sequence = [record['_source']['@timestamp'] for record in result['hits']['hits']]
    check_obtained_records(metrics_sequence, timestamp_sequence)
    return metrics_sequence, timestamp_sequence


def anomaly_detection(metrics_list: List, timestamp_list: List) -> bool:
    pass


def send_alert():
    pass
    

def main() -> None:
    elasticsearch = Elasticsearch(Config.ELASTICSEARCH_URL)
    metrics_sequence, timestamp_sequence = search_metrics_sequence(elasticsearch)
    elasticsearch.close()
    

if __name__ == '__main__':
    logger.debug('----------------------------Config----------------------------')
    for key, value in Config.__dict__.items():
        logger.debug(f'{key}: {value}')
    logger.debug('--------------------------------------------------------------')
    
    main()