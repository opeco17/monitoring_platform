import datetime
import unittest

from anomaly_detection import AnomalyDetector
from config import Config
from tests.utils import *


class TestAnomalyDetector(unittest.TestCase):
    
    def test_check_record_num_is_enough_success1(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence1()
        record_num_is_enough = AnomalyDetector.check_record_num_is_enough(timestamp_metrics_sequence)
        self.assertTrue(record_num_is_enough)
        
    def test_check_record_num_is_enough_success2(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence2()
        record_num_is_enough = AnomalyDetector.check_record_num_is_enough(timestamp_metrics_sequence)
        self.assertTrue(record_num_is_enough)
        
    def test_check_record_num_is_enough_success3(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence3()
        record_num_is_enough = AnomalyDetector.check_record_num_is_enough(timestamp_metrics_sequence)
        self.assertTrue(record_num_is_enough)
        
    def test_check_record_num_is_enough_failure1(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence4()
        record_num_is_enough = AnomalyDetector.check_record_num_is_enough(timestamp_metrics_sequence)
        self.assertFalse(record_num_is_enough)
        
    def test_fill_missing_value_success1(self):
        sparse_timestamp_metrics_sequence, dense_timestamp_metrics_sequence = get_sparse_and_dense_timestamp_metrics1()
        filled_timestamp_metrics_sequence = AnomalyDetector.fill_missing_value(sparse_timestamp_metrics_sequence)
        self.assertEqual(filled_timestamp_metrics_sequence, dense_timestamp_metrics_sequence)
        
    def test_get_check_metrics_increase_success1(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence1()
        metrics_increase = AnomalyDetector.check_metrics_increase(timestamp_metrics_sequence)
        self.assertFalse(metrics_increase)
        
    def test_get_check_metrics_increase_failure1(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence5()
        metrics_increase = AnomalyDetector.check_metrics_increase(timestamp_metrics_sequence)
        self.assertTrue(metrics_increase)
        
    def test_get_latest_time1(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence1()
        timestamp_sequence, _ = AnomalyDetector._timestamp_metrics_unzip(timestamp_metrics_sequence)
        latest_time = AnomalyDetector._get_latest_time(timestamp_sequence)
        self.assertEqual(latest_time, timestamp_sequence[0])
        
    def test_get_latest_time2(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence4()
        timestamp_sequence, _ = AnomalyDetector._timestamp_metrics_unzip(timestamp_metrics_sequence)
        latest_time = AnomalyDetector._get_latest_time(timestamp_sequence)
        current_time = datetime.datetime.now().replace(second=0).replace(microsecond=0)
        self.assertEqual(latest_time, current_time - datetime.timedelta(minutes=1))