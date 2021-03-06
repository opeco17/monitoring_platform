from retry import retry
import sys
from typing import Dict

import requests
from requests.models import Response
from requests.exceptions import ConnectionError, HTTPError, Timeout

from logger import logger
from config import Config
from exceptions import *


class MetricsGetter:

    @classmethod
    def get_page_speed_metrics(cls) -> Dict:
        """Get metrics from Google PageSpeed Insights API in json"""
        try:
            response = cls.__get_response_with_retry()
        except (ConnectionError, HTTPError, Timeout):
            raise GetMetricsError
        else:
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
    
    @classmethod
    @retry(exceptions=(ConnectionError, HTTPError, Timeout), tries=5, delay=3, logger=logger)
    def __get_response_with_retry(cls) -> Response:
        params = {
            'url': Config.TARGET_WEB_PAGE_URI,
            'strategy': Config.PLATFORM
        }
        response = requests.get(Config.PAGE_SPEED_INSIGHTS_API_URI, params=params)
        logger.info(f'Status Code from PageSpeed Insights API: {response.status_code}')
        response.raise_for_status()
        return response