from typing import Dict, List
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
        
    @mock.patch('connect_es.Elasticsearch')
    def test_constructor_success(self, mock):
        mock.return_value = None
        elasticsearch = ElasticsearchConnector()
        
    @mock.patch('connect_es.Elasticsearch')
    def test_constructor_failure(self, mock):
        mock.side_effect = LocationValueError
        with self.assertRaises(IncorrectElasticsearchURLError):
            elasticsearch = ElasticsearchConnector()
    
    def test_create_index_template_success1(self):
        elasticsearch_connector = ElasticsearchConnector()
        client_mock = mock.MagicMock()
        client_mock.indices.exists_index_template.return_value = True
        with mock.patch.object(elasticsearch_connector, '_client', client_mock):
            elasticsearch_connector.create_index_template()
            
    def test_create_index_template_success2(self):
        elasticsearch_connector = ElasticsearchConnector()
        client_mock = mock.MagicMock()
        client_mock.indices.exists_index_template.return_value = False
        client_mock.indices.put_index_template.return_value = None
        with mock.patch.object(elasticsearch_connector, '_client', client_mock):
            elasticsearch_connector.create_index_template()
            
    def test_create_index_template_failure1(self):
        elasticsearch_connector = ElasticsearchConnector()
        client_mock = mock.MagicMock()
        client_mock.indices.exists_index_template.side_effect = ConnectionError
        with mock.patch.object(elasticsearch_connector, '_client', client_mock):
            with self.assertRaises(IndexPatternConfirmError):
                elasticsearch_connector.create_index_template()
                
    def test_create_index_template_failure2(self):
        elasticsearch_connector = ElasticsearchConnector()
        client_mock = mock.MagicMock()
        client_mock.indices.exists_index_template.return_value = False
        client_mock.indices.put_index_template.side_effect = ConnectionError
        with mock.patch.object(elasticsearch_connector, '_client', client_mock):
            with self.assertRaises(IndexPatternCreationError):
                elasticsearch_connector.create_index_template()
                
    def test_insert_success(self):
        elasticsearch_connector = ElasticsearchConnector()

        prepare_data_for_insert_mock = mock.MagicMock()
        prepare_data_for_insert_mock.return_value = '', {}
        
        client_mock = mock.MagicMock()
        client_mock.index.return_value = None
        
        with mock.patch.object(elasticsearch_connector, '_prepare_data_for_insert', prepare_data_for_insert_mock), \
            mock.patch.object(elasticsearch_connector, '_client', client_mock):
            elasticsearch_connector.insert({})

    def test_insert_failure(self):
        elasticsearch_connector = ElasticsearchConnector()
        
        prepare_data_for_insert_mock = mock.MagicMock()
        prepare_data_for_insert_mock.return_value = 'index_name', {}
        
        client_mock = mock.MagicMock()
        client_mock.index.side_effect = ConnectionError
        
        with mock.patch.object(elasticsearch_connector, '_prepare_data_for_insert', prepare_data_for_insert_mock), \
            mock.patch.object(elasticsearch_connector, '_client', client_mock):
            with self.assertRaises(MetricsInsertError):
                elasticsearch_connector.insert({})
                
    @mock.patch('connect_es.bulk')
    @mock.patch('connect_es.ElasticsearchConnector._prepare_data_for_insert')
    def test_bulk_insert_success(self, prepare_data_for_insert_mock, bulk_mock):
        prepare_data_for_insert_mock.return_value = 'index_name', {}
        bulk_mock.return_value = None
        
        elasticsearch_connector = ElasticsearchConnector()
        elasticsearch_connector.bulk_insert([])
            
    @mock.patch('connect_es.bulk')
    @mock.patch('connect_es.ElasticsearchConnector._prepare_data_for_insert')
    def test_bulk_insert_failure(self, prepare_data_for_insert_mock, bulk_mock):
        prepare_data_for_insert_mock.return_value = 'index_name', {}
        bulk_mock.side_effect = ConnectionError

        elasticsearch_connector = ElasticsearchConnector()
        with self.assertRaises(MetricsInsertError):
            elasticsearch_connector.bulk_insert([])
                
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
            
    def test_prepare_data_for_insert_success(self):
        elasticsearch_connector = ElasticsearchConnector()
        index_name, body = elasticsearch_connector._prepare_data_for_insert({})
        self.assertIsInstance(index_name, str)
        self.assertIsInstance(body, Dict)
        self.assertIsInstance(body['@timestamp'], str)
        
    def test_prepare_data_for_bulk_insert(self):
        elasticsearch_connector = ElasticsearchConnector()
        generator = elasticsearch_connector._prepare_data_for_bulk_insert([{}, {}, {}])
        for body in generator:
            self.assertIsInstance(body, Dict)
            self.assertIsInstance(body['_index'], str)
            self.assertIsInstance(body['@timestamp'], str)