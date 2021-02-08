import json
import sys
from typing import Dict

from elasticsearch import Elasticsearch
import elasticsearch
import requests
from requests.models import Response
from requests.exceptions import HTTPError
from retry import retry

from config import Config
from logger import get_logger


logger = get_logger()


@retry(exceptions=HTTPError, tries=5, delay=3, backoff=2, logger=logger)
def get_response() -> Response:
    params = {
        'url': Config.TARGET_WEB_PAGE_URI,
        'strategy': Config.PLATFORM
    }
    response = requests.get(Config.PAGE_SPEED_INSIGHTS_API_URI, params=params)
    logger.info(f'Status Code: {response.status_code}')
    response.raise_for_status()
    return response


def get_page_speed_metrics() -> Dict:
    """Get metrics from Google PageSpeed Insights API in json"""
    try:
        response = get_response()
        body = response.json()
        all_metrics = body['lighthouseResult']['audits']
        
        extract_value = lambda metric_type: all_metrics[metric_type]['numericValue']
        metrics = {
            'server_response_time': extract_value('server-response-time'),
            'time_to_interactive': extract_value('interactive'),
            'speed_index': extract_value('speed-index'),
            'first_contentful_paint': extract_value('first-contentful-paint')
        }        
        return metrics
        
    except HTTPError as http_error:
        logger.error('Cannot get page speed metrics due to HTTPError.')
        sys.exit(1)
        
    except KeyError as key_error:
        logger.error(f'Cannot extract metrics due to KeyError.')
        logger.error(f'Wrong key name: {key_error}')
        sys.exit(1)
    

def create_index_template(elasticsearch: Elasticsearch) -> None:
    """Create index template if not exists"""
    exist_index_template = elasticsearch.indices.exists_index_template(name=Config.INDEX_TEMPLATE_NAME)
    if not exist_index_template:
        return
    
    with open(Config.INDEX_TEMPLATE_PATH) as index_template_file:
        index_template = json.load(index_template_file)
        
    index_template['index_patterns'].append(f'{Config.INDEX_PREFIX}*')
    result = elasticsearch.indices.put_index_template(name=Config.INDEX_TEMPLATE_NAME, body=index_template)
    if result.get('acknowledged') is True:
        return

    logger.error('Failed to create index pattern.')
    raise Exception
    

def insert_elasticsearch(elasticsearch: Elasticsearch, metrics: Dict) -> None:
    pass
    

def main():
    metrics = get_page_speed_metrics()
    
    elasticsearch = Elasticsearch(Config.ELASTICSEARCH_URL)
    create_index_template(elasticsearch)
    insert_elasticsearch(elasticsearch, metrics)
    
    
    

if __name__ == '__main__':
    logger.debug('----------------------------Config----------------------------')
    for key, value in Config.__dict__.items():
        logger.debug(f'{key}: {value}')
    logger.debug('--------------------------------------------------------------')
    
    main()