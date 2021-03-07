from contextlib import contextmanager
import datetime
from typing import List

from config import Config


@contextmanager
def config_setup(config_attrs: List):
    try:
        old_config_attrs = [(key, getattr(Config, key)) for key, _ in config_attrs]
        for key, value in config_attrs:
            setattr(Config, key, value)
        yield None
    finally:
        for key, value in old_config_attrs:
            setattr(Config, key, value)
            

def get_timestamp_metrics_sequence_correct1():
    now = datetime.datetime.now()
    base_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    timestamp_metrics_sequence = []
    for i in range(Config.METRICS_SEQUENCE_LENGTH):
        delta = datetime.timedelta(minutes=i)
        timestamp_metrics_sequence.append((base_date - delta, 100.0))
    return timestamp_metrics_sequence


def get_timestamp_metrics_sequence_correct2():
    now = datetime.datetime.now()
    base_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    timestamp_metrics_sequence = []
    for i in range(Config.METRICS_SEQUENCE_LENGTH):
        delta = datetime.timedelta(minutes=i+Config.ALLOWABLE_NUMBER_OF_FAILURES-2)
        timestamp_metrics_sequence.append((base_date - delta, 100.0))
    return timestamp_metrics_sequence


def get_timestamp_metrics_sequence_correct3():
    now = datetime.datetime.now()
    base_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    timestamp_metrics_sequence = []
    for i in range(Config.METRICS_SEQUENCE_LENGTH):
        delta = datetime.timedelta(minutes=i*2)
        timestamp_metrics_sequence.append((base_date - delta, 100.0))
    return timestamp_metrics_sequence


def get_timestamp_metrics_sequence_incorrect1():
    now = datetime.datetime.now()
    base_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    timestamp_metrics_sequence = []
    for i in range(Config.METRICS_SEQUENCE_LENGTH):
        delta = datetime.timedelta(minutes=i+Config.ALLOWABLE_NUMBER_OF_FAILURES-1)
        timestamp_metrics_sequence.append((base_date - delta, 100.0))
    return timestamp_metrics_sequence


def get_sparse_and_dense_timestamp_metrics_sequence1():
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