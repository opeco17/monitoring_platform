from contextlib import contextmanager
import datetime
from typing import Any, List

from config import Config
from requests.exceptions import HTTPError


class ResponseMock:
    
    def __init__(self, status_code: int, body: Any):
        self.status_code = status_code
        self.body = body
        
    def raise_for_status(self):
        if 200 <= self.status_code <= 299:
            return
        raise HTTPError
    

@contextmanager
def config_setup(config_attrs: List) -> None:
    """Change config value temporary in config_setup context manager"""
    try:
        old_config_attrs = [(key, getattr(Config, key)) for key, _ in config_attrs]
        for key, value in config_attrs:
            setattr(Config, key, value)
        yield None
    finally:
        for key, value in old_config_attrs:
            setattr(Config, key, value)
    

def get_timestamp_metrics_sequence1() -> List:
    """
        Return [(current_time, 100.0), (1minutes_ago, 100.0), (2minutes_ago, 100.0), ...]
    """
    now = datetime.datetime.now()
    base_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    timestamp_metrics_sequence = []
    for i in range(Config.METRICS_SEQUENCE_LENGTH):
        delta = datetime.timedelta(minutes=i)
        timestamp_metrics_sequence.append((base_date - delta, 100.0))
    return timestamp_metrics_sequence


def get_timestamp_metrics_sequence2() -> List:
    """
        If Config.ALLOWABLE_NUMBER_OF_FAILURES is 3,
        return [(2minutes_ago, 100.0), (3minutes_ago, 100.0), (4minutes_ago, 100.0), ...]
    """
    now = datetime.datetime.now()
    base_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    timestamp_metrics_sequence = []
    for i in range(Config.METRICS_SEQUENCE_LENGTH):
        delta = datetime.timedelta(minutes=i+Config.ALLOWABLE_NUMBER_OF_FAILURES-1)
        timestamp_metrics_sequence.append((base_date - delta, 100.0))
    return timestamp_metrics_sequence


def get_timestamp_metrics_sequence3() -> List:
    """
        Return [(current_time, 100.0), (2minutes_ago, 100.0), (4minutes_ago, 100.0), ...]
    """
    now = datetime.datetime.now()
    base_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    timestamp_metrics_sequence = []
    for i in range(Config.METRICS_SEQUENCE_LENGTH):
        delta = datetime.timedelta(minutes=i*2)
        timestamp_metrics_sequence.append((base_date - delta, 100.0))
    return timestamp_metrics_sequence


def get_timestamp_metrics_sequence4() -> List:
    """
        If Config.ALLOWABLE_NUMBER_OF_FAILURES is 3,
        return [(4minutes_ago, 100.0), (5minutes_ago, 100.0), (6minutes_ago, 100.0), ...]
    """
    now = datetime.datetime.now()
    base_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    timestamp_metrics_sequence = []
    for i in range(Config.METRICS_SEQUENCE_LENGTH):
        delta = datetime.timedelta(minutes=i+Config.ALLOWABLE_NUMBER_OF_FAILURES+1)
        timestamp_metrics_sequence.append((base_date - delta, 100.0))
    return timestamp_metrics_sequence

def get_timestamp_metrics_sequence5() -> List:
    """
        If Config.ALLOWABLE_NUMBER_OF_FAILURES is 3,
        return [(current_time, 1000.0), (1minutes_ago, 1000.0), (2minutes_ago, 1000.0), (3minutes_ago, 100.0), ...]
    """
    now = datetime.datetime.now()
    base_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    timestamp_metrics_sequence = []
    for i in range(Config.METRICS_SEQUENCE_LENGTH):
        if i < 3:
            metrics = 1000.0
        else:
            metrics = 100.0
        delta = datetime.timedelta(minutes=i)
        timestamp_metrics_sequence.append((base_date - delta, metrics))
    return timestamp_metrics_sequence

def get_sparse_and_dense_timestamp_metrics1() -> List:
    """
        Sparse timestamp metrics: [(current_time, 1000.0), (2minutes_ago, 1000.0), (4minutes_ago, 1000.0), ...]
        Dense timestamp metrics: [(current_time, 1000.0), (1minutes_ago, 1000.0), (2minutes_ago, 1000.0), ...]
    """
    now = datetime.datetime.now()
    base_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    sparse_timestamp_metrics_sequence = []
    dense_timestamp_metrics_sequence = []
    for i in range(Config.METRICS_SEQUENCE_LENGTH):
        delta = datetime.timedelta(minutes=i*2)
        sparse_timestamp_metrics_sequence.append((base_date - delta, 100.0))
        
        delta = datetime.timedelta(minutes=i)
        dense_timestamp_metrics_sequence.append((base_date - delta, 100.0))
    return sparse_timestamp_metrics_sequence, dense_timestamp_metrics_sequence