from datetime import time
from typing import Dict, List, Tuple
import unittest

from elasticsearch import Elasticsearch
from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import Config
from exceptions import *
from connect_es import ElasticsearchConnector
from tests.utils import config_setup
        
        
class TestConnectES(unittest.TestCase):
    
    def setUp(self):
        self.elasticsearch_connector = ElasticsearchConnector()
        
    def test_constructor_success(self):
        elasticsearch = ElasticsearchConnector()
        self.assertIsInstance(elasticsearch._client, Elasticsearch)
        
    def test_constructor_failure(self):
        config_attrs = [('ELASTICSEARCH_URL', '')]
        with config_setup(config_attrs):
            with self.assertRaises(IncorrectElasticsearchURLError):
                elasticsearch = ElasticsearchConnector()
    
    def test_get_timestamp_metrics_sequence_success(self):
        timestamp_metrics_sequence = self.elasticsearch_connector.get_timestamp_metrics_sequence('https://www.google.com/')
        self.assertIsInstance(timestamp_metrics_sequence, List)
        self.assertIsInstance(timestamp_metrics_sequence[0], Tuple)
        
    def test_get_timestamp_metrics_sequence_failure(self):
        with self.assertRaises(GetTimestampMetricsSequenceError):
            timestamp_metrics_sequence = self.elasticsearch_connector.get_timestamp_metrics_sequence('')
            
    def test_create_search_query_success(self):
        target_web_page_url = 'https://www.google.com/'
        search_query = self.elasticsearch_connector._create_search_query(target_web_page_url)
        self.assertEqual(search_query['query']['bool']['filter'][0]['term']['target_url'], target_web_page_url)
        self.assertIn(search_query['query']['bool']['filter'][1]['term']['platform'], ['desktop', 'mobile'])
        self.assertIsInstance(search_query['aggs']['histogram']['aggs']['metrics_average']['avg']['field'], str)
        self.assertIsInstance(search_query['aggs']['histogram']['aggs']['timestamp_sort']['bucket_sort']['size'], int)