import json
import unittest

from requests.exceptions import HTTPError, MissingSchema

from exceptions import *
from send_alert import AlertSender
from tests.utils import *


class TestSendAlert(unittest.TestCase):
    
    def test_send_alert_for_record_not_enough_success(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence1()
        AlertSender.send_alert_for_record_not_enough('https://google.com/', timestamp_metrics_sequence)
        
    def test_send_alert_for_record_not_enough_failure1(self):
        config_attrs = [('WEBHOOK_URL', 'some_wrong_word')]
        with config_setup(config_attrs):
            with self.assertRaises(SendAlertByWebhookError):
                timestamp_metrics_sequence = get_timestamp_metrics_sequence1()
                AlertSender.send_alert_for_record_not_enough('https://google.com/', timestamp_metrics_sequence)
                
    def test_send_alert_for_metrics_increase_success(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence1()
        AlertSender.send_alert_for_metrics_increase('https://google.com/', timestamp_metrics_sequence)
        
    def test_send_alert_for_metrics_increase_failure1(self):
        config_attrs = [('WEBHOOK_URL', 'some_wrong_word')]
        with config_setup(config_attrs):
            with self.assertRaises(SendAlertByWebhookError):
                timestamp_metrics_sequence = get_timestamp_metrics_sequence1()
                AlertSender.send_alert_for_metrics_increase('https://google.com/', timestamp_metrics_sequence)
                
    def test_send_alert_success(self):
        AlertSender._send_alert('text', 'username')
        
    def test_send_alert_failure(self):
        config_attrs = [('WEBHOOK_URL', 'some_wrong_word')]
        with config_setup(config_attrs):
            with self.assertRaises(SendAlertByWebhookError):
                AlertSender._send_alert('text', 'username')
                
    def test_post_request_with_retry_success(self):
        data = json.dumps({
            'text': 'text', 
            'username': 'username'
        })
        AlertSender._post_request_with_retry(data)
        
    def test_post_request_with_retry_failure1(self):
        with self.assertRaises(HTTPError):
            AlertSender._post_request_with_retry('data')
            
    def test_post_request_with_retry_failure2(self):
        data = json.dumps({
            'text': 'text', 
            'username': 'username'
        })
        config_attrs = [('WEBHOOK_URL', 'some_wrong_word')]
        with config_setup(config_attrs):
            with self.assertRaises(MissingSchema):
                AlertSender._post_request_with_retry(data)