from retry import retry
from typing import Dict, List

from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
import requests
from requests.models import Response
from requests.exceptions import ConnectionError, HTTPError, Timeout

from logger import logger
from config import Config
from exceptions import *
from utils import *


class MetricsGetter:

    @classmethod
    def get_page_speed_metrics(cls, web_page_url: str) -> Dict:
        """Get metrics from Google PageSpeed Insights API in json"""
        try:
            response = cls._get_request_with_retry(web_page_url)
        except (ConnectionError, HTTPError, Timeout):
            raise GetMetricsError
        else:
            body = response.json()
            all_metrics = body['lighthouseResult']['audits']
            
            extract_value = lambda metric_type: all_metrics[metric_type]['numericValue']
            metrics = {
                'target_url': web_page_url,
                'platform': Config.PLATFORM,
                'server_response_time': extract_value('server-response-time'),
                'time_to_interactive': extract_value('interactive'),
                'speed_index': extract_value('speed-index'),
                'first_contentful_paint': extract_value('first-contentful-paint')
            }
            return metrics
        
    @classmethod
    def get_multiple_page_speed_metrics(cls, web_page_url_list: List) -> List:
        max_workers = min(len(web_page_url_list), 5)
        metrics_list = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            mappings = {executor.submit(cls.get_page_speed_metrics, web_page_url): web_page_url for web_page_url in web_page_url_list}
            for future in futures.as_completed(mappings):
                result = future.result()
                metrics_list.append(result)
        return metrics_list
    
    @classmethod
    @retry(exceptions=(ConnectionError, HTTPError, Timeout), tries=5, delay=3, logger=logger)
    def _get_request_with_retry(cls, web_page_url: str) -> Response:
        params = {
            'url': web_page_url,
            'strategy': Config.PLATFORM
        }
        response = requests.get(Config.PAGE_SPEED_INSIGHTS_API_URI, params=params)
        logger.info(f'Status Code from PageSpeed Insights API: {response.status_code}')
        response.raise_for_status()
        return response