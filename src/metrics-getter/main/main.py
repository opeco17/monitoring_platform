import sys
from typing import Dict

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
            'speed_index': extract_value('speed-index')
        }        
        return metrics
        
    except HTTPError as http_error:
        logger.error('Cannot get page speed metrics due to HTTPError.')
        sys.exit(1)
        
    except KeyError as key_error:
        logger.error(f'Cannot extract metrics due to KeyError.')
        logger.error(f'Wrong key name: {key_error}')
        sys.exit(1)
    
    
def insert_elasticsearch(metrics: Dict):
    pass
    

def main():
    metrics = get_page_speed_metrics()
    
    

if __name__ == '__main__':
    main()