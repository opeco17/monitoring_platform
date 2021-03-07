import unittest

from anomaly_detection import AnomalyDetector
from config import Config
from tests.utils import *


class TestAnomalyDetector(unittest.TestCase):
    
    def test_check_record_num_is_enough_success1(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence_correct1()
        record_num_is_enough = AnomalyDetector.check_record_num_is_enough(timestamp_metrics_sequence)
        self.assertTrue(record_num_is_enough)
        
    def test_check_record_num_is_enough_success2(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence_correct2()
        record_num_is_enough = AnomalyDetector.check_record_num_is_enough(timestamp_metrics_sequence)
        self.assertTrue(record_num_is_enough)
        
    # def test_check_record_num_is_enough_success3(self):
    #     timestamp_metrics_sequence = get_timestamp_metrics_sequence_correct3()
    #     record_num_is_enough = AnomalyDetector.check_record_num_is_enough(timestamp_metrics_sequence)
    #     self.assertTrue(record_num_is_enough)
        
    def test_check_record_num_is_enough_failure1(self):
        timestamp_metrics_sequence = get_timestamp_metrics_sequence_incorrect1()
        record_num_is_enough = AnomalyDetector.check_record_num_is_enough(timestamp_metrics_sequence)
        self.assertFalse(record_num_is_enough)
        
    def test_fill_missing_value_success1(self):
        sparse_timestamp_metrics_sequence, dense_timestamp_metrics_sequence = get_sparse_and_dense_timestamp_metrics_sequence1()
        filled_timestamp_metrics_sequence = AnomalyDetector.fill_missing_value(sparse_timestamp_metrics_sequence)
        self.assertEqual(filled_timestamp_metrics_sequence, dense_timestamp_metrics_sequence)