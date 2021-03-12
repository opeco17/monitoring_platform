from datetime import datetime, time
import json
from typing import Dict, List, Tuple
import unittest
from unittest import mock
from urllib3.exceptions import LocationValueError

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

from config import Config
from exceptions import *
from connect_es import ElasticsearchConnector
from tests.utils import config_setup
        
        
class TestConnectES(unittest.TestCase):
    
    def setUp(self):
        with open('./tests/json/es_search_result.json') as file:
            self.search_result = json.load(file)
    
    @mock.patch('connect_es.Elasticsearch')
    def test_constructor_success(self, mock):
        mock.return_value = None
        elasticsearch = ElasticsearchConnector()
        
    @mock.patch('connect_es.Elasticsearch')
    def test_constructor_failure(self, mock):
        mock.side_effect = LocationValueError
        with self.assertRaises(IncorrectElasticsearchURLError):
            elasticsearch = ElasticsearchConnector()
            
    @mock.patch('connect_es.Elasticsearch.search')
    @mock.patch('connect_es.ElasticsearchConnector._create_search_query')
    def test_get_timestamp_metrics_sequence_success(self, create_search_query_mock, search_mock):
        create_search_query_mock.return_value = None
        search_mock.return_value = self.search_result
        
        elasticsearch_connector = ElasticsearchConnector()
        timestamp_metrics_sequence = elasticsearch_connector.get_timestamp_metrics_sequence('url')
        self.assertIsInstance(timestamp_metrics_sequence, List)
        self.assertIsInstance(timestamp_metrics_sequence[0], Tuple)
        self.assertIsInstance(timestamp_metrics_sequence[0][0], datetime)
        self.assertIsInstance(timestamp_metrics_sequence[0][1], float)
        
    @mock.patch('connect_es.Elasticsearch.search')
    @mock.patch('connect_es.ElasticsearchConnector._create_search_query')
    def test_get_timestamp_metrics_sequence_failure1(self, create_search_query_mock, search_mock):
        create_search_query_mock.return_value = None
        search_mock.return_value = {'aggregations': {'histogram': {'buckets': None}}}
        
        elasticsearch_connector = ElasticsearchConnector()
        with self.assertRaises(GetTimestampMetricsSequenceError):
            elasticsearch_connector.get_timestamp_metrics_sequence('url')
            
    @mock.patch('connect_es.Elasticsearch.search')
    @mock.patch('connect_es.ElasticsearchConnector._create_search_query')
    def test_get_timestamp_metrics_sequence_failure2(self, create_search_query_mock, search_mock):
        create_search_query_mock.return_value = None
        search_mock.side_effect = ConnectionError
        
        elasticsearch_connector = ElasticsearchConnector()
        with self.assertRaises(GetTimestampMetricsSequenceError):
            elasticsearch_connector.get_timestamp_metrics_sequence('url')  
    
    @mock.patch('connect_es.Elasticsearch.close')
    def test_close_success(self, close_mock):
        close_mock.return_value = None
        
        elasticsearch_connector = ElasticsearchConnector()
        elasticsearch_connector.close()
    
    @mock.patch('connect_es.Elasticsearch.close')
    def test_close_failure(self, close_mock):
        close_mock.side_effect = ConnectionError
        
        elasticsearch_connector = ElasticsearchConnector()
        with self.assertRaises(ConnectionCloseError):
            elasticsearch_connector.close()
            
    def test_create_search_query_success(self):
        target_web_page_url = 'https://www.google.com/'
        elasticsearch_connector = ElasticsearchConnector()

        search_query = elasticsearch_connector._create_search_query(target_web_page_url)
        self.assertEqual(search_query['query']['bool']['filter'][0]['term']['target_url'], target_web_page_url)
        self.assertIn(search_query['query']['bool']['filter'][1]['term']['platform'], ['desktop', 'mobile'])
        self.assertIsInstance(search_query['aggs']['histogram']['aggs']['metrics_average']['avg']['field'], str)
        self.assertIsInstance(search_query['aggs']['histogram']['aggs']['timestamp_sort']['bucket_sort']['size'], int)