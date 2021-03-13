import json
from numbers import Number
from typing import Dict, List
import unittest
from unittest import mock

from requests.exceptions import HTTPError

from config import Config
from exceptions import *
from get_metrics import MetricsGetter
from tests.utils import *
        

class TestMetricsGetter(unittest.TestCase):
    
    def setUp(self):
        self.page_speed_json_bodies = {}
        for web_page_name in ['google', 'amazon', 'facebook', 'apple', 'invalid_url']:
            web_page_url = f'https://{web_page_name}.com'
            with open(f'./tests/json/page_speed_api/{web_page_name}.json') as json_file:
                self.page_speed_json_bodies[web_page_name] = (web_page_url, json.load(json_file))
    
    @mock.patch('get_metrics.MetricsGetter._get_request_with_retry')
    def test_get_page_speed_metrics_success(self, mock):
        url, body = self.page_speed_json_bodies['google']
        mock.return_value = ResponseMock(200, body)
        
        metrics = MetricsGetter.get_page_speed_metrics(url)
        self.check_metrics(metrics)
        
    @mock.patch('get_metrics.MetricsGetter._get_request_with_retry')
    def test_get_page_speed_metrics_failure(self, mock):
        mock.side_effect = HTTPError
        
        with self.assertRaises(GetMetricsError):
            MetricsGetter.get_page_speed_metrics('invalid_url')
            
    @mock.patch('get_metrics.MetricsGetter._get_request_with_retry')
    def test_get_multiple_page_speed_metrics_success(self, mock):
        urls, bodies = zip(*[self.page_speed_json_bodies[name] for name in ['google', 'amazon', 'facebook', 'apple']])
        urls, bodies = list(urls), list(bodies)
        mock.side_effect = [ResponseMock(200, body) for body in bodies]
        
        metrics_list = MetricsGetter.get_multiple_page_speed_metrics(urls)
        for metrics in metrics_list:
            self.check_metrics(metrics)
            
    @mock.patch('get_metrics.MetricsGetter._get_request_with_retry')
    def test_get_multiple_page_speed_metrics_failure(self, mock):
        urls, bodies = zip(*[self.page_speed_json_bodies[name] for name in ['google', 'amazon', 'facebook', 'apple']])
        invalid_url, invalid_body = self.page_speed_json_bodies['invalid_url']
        urls = list(urls) + [invalid_url]
        responses = [ResponseMock(200, body) for body in bodies] + [HTTPError]
        mock.side_effect = responses
        
        with self.assertRaises(GetMetricsError):
            MetricsGetter.get_multiple_page_speed_metrics(urls)
    
    @mock.patch('get_metrics.requests.get')
    def test_get_request_with_retry_success(self, mock):
        url, body = self.page_speed_json_bodies['google']
        mock.return_value = ResponseMock(200, body)
        
        response = MetricsGetter._get_request_with_retry(url)
        response_body = response.json()
        self.assertIsInstance(response_body, Dict)
        
    @mock.patch('get_metrics.requests.get')
    def test_get_request_with_retry_failure(self, mock):
        url, body = self.page_speed_json_bodies['invalid_url']
        mock.return_value = ResponseMock(500, body)
        
        with self.assertRaises(HTTPError):
            MetricsGetter._get_request_with_retry(url)
    
    def check_metrics(self, metrics):
        self.assertIsInstance(metrics, Dict)
        self.assertIsInstance(metrics['target_url'], str)
        self.assertIn(metrics['platform'], {'desktop', 'mobile'})
        self.assertIsInstance(metrics['server_response_time'], Number)
        self.assertIsInstance(metrics['time_to_interactive'], Number)
        self.assertIsInstance(metrics['speed_index'], Number)
        self.assertIsInstance(metrics['first_contentful_paint'], Number)