import json
import unittest
from unittest import mock

from requests.exceptions import HTTPError, MissingSchema

from exceptions import *
from send_alert import AlertSender
from tests.utils import *


class TestSendAlert(unittest.TestCase):
    
    @mock.patch('send_alert.requests.post')
    def test_send_alert_for_record_not_enough_success(self, mock):
        mock.return_value = ResponseMock(200, None)
        
        timestamp_metrics_sequence = get_timestamp_metrics_sequence1()
        AlertSender.send_alert_for_record_not_enough('url', timestamp_metrics_sequence)
        
    @mock.patch('send_alert.requests.post')
    def test_send_alert_for_record_not_enough_failure(self, mock):
        mock.return_value = ResponseMock(404, None)
        
        timestamp_metrics_sequence = get_timestamp_metrics_sequence1()
        with self.assertRaises(SendAlertByWebhookError):
            AlertSender.send_alert_for_record_not_enough('url', timestamp_metrics_sequence)
                
    @mock.patch('send_alert.requests.post')
    def test_send_send_alert_for_metrics_increase_success(self, mock):
        mock.return_value = ResponseMock(200, None)
        
        timestamp_metrics_sequence = get_timestamp_metrics_sequence1()
        AlertSender.send_alert_for_metrics_increase('url', timestamp_metrics_sequence)
        
    @mock.patch('send_alert.requests.post')
    def test_send_alert_for_metrics_increase_failure(self, mock):
        mock.return_value = ResponseMock(404, None)
        
        timestamp_metrics_sequence = get_timestamp_metrics_sequence1()
        with self.assertRaises(SendAlertByWebhookError):
            AlertSender.send_alert_for_metrics_increase('url', timestamp_metrics_sequence)
                   
    @mock.patch('send_alert.requests.post')
    def test_send_alert_success(self, mock):
        mock.return_value = ResponseMock(200, None)

        AlertSender._send_alert('text', 'username')
        
    @mock.patch('send_alert.requests.post')
    def test_send_alert_failure(self, mock):
        mock.return_value = ResponseMock(404, None)
        
        with self.assertRaises(SendAlertByWebhookError):
            AlertSender._send_alert('text', 'username')
            
    @mock.patch('send_alert.requests.post')
    def test_post_request_with_retry_success(self, mock):
        mock.return_value = ResponseMock(200, None)
        
        AlertSender._post_request_with_retry('data')
        
    @mock.patch('send_alert.requests.post')
    def test_post_request_with_retry_failure(self, mock):
        mock.return_value = ResponseMock(404, None)
        
        with self.assertRaises(HTTPError):
            AlertSender._post_request_with_retry('data')