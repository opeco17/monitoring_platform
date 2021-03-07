from typing import Dict, List
import unittest

from elasticsearch import Elasticsearch
from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import Config
from exceptions import *
from get_metrics import MetricsGetter
from connect_es import ElasticsearchConnector
from tests.utils import config_setup
        
        
class TestConnectES(unittest.TestCase):
    
    def setUp(self):
        self.elasticsearch_connector = ElasticsearchConnector()
        self.elasticsearch_connector.create_index_template()
        
    def test_constructor_success(self):
        elasticsearch = ElasticsearchConnector()
        self.assertIsInstance(elasticsearch._client, Elasticsearch)
        
    def test_constructor_failure(self):
        config_attrs = [('ELASTICSEARCH_URL', '')]
        with config_setup(config_attrs):
            with self.assertRaises(IncorrectElasticsearchURLError):
                elasticsearch = ElasticsearchConnector()
        
    def test_insert_success(self):
        self.elasticsearch_connector.create_insert()