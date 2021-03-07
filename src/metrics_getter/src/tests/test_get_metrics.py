from typing import Dict, List
import unittest

from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import Config
from exceptions import *
from get_metrics import MetricsGetter
from tests.utils import config_setup
        

class TestMetricsGetter(unittest.TestCase):
    
    def setUp(self):
        self.correct_url = 'https://google.com'
        self.incorrect_url = 'some_wrong_word'
        self.correct_url_list = ['https://google.com', 'https://www.amazon.com/', 'https://www.facebook.com/', 'https://www.apple.com/']
        self.incorrect_url_list = ['some_wrong_word1', 'some_wrong_word2', 'some_wrong_word3', 'some_wrong_word4']
    
    def test_get_request_with_retry_for_desktop_success(self):
        config_attrs = [('PLATFORM', 'desktop')]
        with config_setup(config_attrs):
            response = MetricsGetter._get_request_with_retry(self.correct_url)
            self.assertEqual(response.status_code, 200)
            
    def test_get_request_with_retry_for_mobile_success(self):
        config_attrs = [('PLATFORM', 'mobile')]
        with config_setup(config_attrs):
            response = MetricsGetter._get_request_with_retry(self.correct_url)
            self.assertEqual(response.status_code, 200)
            
    def test_get_request_with_retry_failure(self):
        with self.assertRaises(HTTPError):
            response = MetricsGetter._get_request_with_retry(self.incorrect_url)
            
    def test_get_page_speed_metrics_for_desktop_success(self):
        config_attrs = [('PLATFORM', 'desktop')]
        with config_setup(config_attrs):
            metrics = MetricsGetter.get_page_speed_metrics(self.correct_url)
            self.assertIsInstance(metrics, Dict)
            
    def test_get_page_speed_metrics_for_mobile_success(self):
        config_attrs = [('PLATFORM', 'mobile')]
        with config_setup(config_attrs):
            metrics = MetricsGetter.get_page_speed_metrics(self.correct_url)
            self.assertIsInstance(metrics, Dict)
            
    def test_get_page_speed_metrics_failure(self):
        with self.assertRaises(GetMetricsError):
            metrics = MetricsGetter.get_page_speed_metrics(self.incorrect_url)
            
    def test_get_multiple_page_speed_metrics_for_desktop_success(self):
        config_attrs = [('PLATFORM', 'desktop')]
        with config_setup(config_attrs):
            metrics_list = MetricsGetter.get_multiple_page_speed_metrics(self.correct_url_list)
            self.assertIsInstance(metrics_list, List)
            self.assertIsInstance(metrics_list[0], Dict)
            
    def test_get_multiple_page_speed_metrics_for_mobile_success(self):
        config_attrs = [('PLATFORM', 'mobile')]
        with config_setup(config_attrs):
            metrics_list = MetricsGetter.get_multiple_page_speed_metrics(self.correct_url_list)
            self.assertIsInstance(metrics_list, List)
            self.assertIsInstance(metrics_list[0], Dict)
            
    def test_get_multiple_page_speed_metrics_failure(self):
        with self.assertRaises(GetMetricsError):
            metrics_list = MetricsGetter.get_multiple_page_speed_metrics(self.incorrect_url_list)