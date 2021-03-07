import datetime
from typing import List, Tuple

from config import Config
from exceptions import *
from logger import logger
from send_alert import AlertSender


class AnomalyDetector:
    
    @classmethod
    def check_record_num_is_enough(cls, timestamp_metrics_sequence: List) -> bool:
        """If there are enough records in sequence, return True"""
        timestamp_sequence, _ = cls._timestamp_metrics_unzip(timestamp_metrics_sequence)
        record_num_is_enough = cls._record_num_is_enough(timestamp_sequence)
        if record_num_is_enough:
            return True

        logger.info('Number of record is not enough')
        return False
    
    @classmethod
    def fill_missing_value(cls, timestamp_metrics_sequence: List) -> List:
        """Fill missing value in sequence with interpolation"""
        timestamp_sequence, metrics_sequence = cls._timestamp_metrics_unzip(timestamp_metrics_sequence)
        latest_time = cls._get_latest_time(timestamp_sequence)
        if timestamp_sequence[0] != latest_time:
            timestamp_sequence.insert(0, latest_time)
            metrics_sequence.insert(0, metrics_sequence[0])
        
        missing_timestamp_list = []
        missing_metrics_list = []
        for i in range(len(timestamp_sequence)-1):
            target_time = timestamp_sequence[i]
            previous_time = timestamp_sequence[i+1]
            while True:
                if target_time == previous_time + datetime.timedelta(minutes=1):
                    break

                target_time -= datetime.timedelta(minutes=1)
                missing_timestamp_list.append(target_time)
                missing_metrics_list.append((metrics_sequence[i-1] + metrics_sequence[i])/2)
                
        filled_timestamp_sequence = timestamp_sequence + missing_timestamp_list
        filled_metrics_sequence = metrics_sequence + missing_metrics_list
        
        # Sort by timestamp sequence
        filled_timestamp_metrics_sequence = sorted(zip(filled_timestamp_sequence, filled_metrics_sequence), reverse=True)
        filled_timestamp_metrics_sequence = filled_timestamp_metrics_sequence[:Config.METRICS_SEQUENCE_LENGTH]
        return filled_timestamp_metrics_sequence
    
    @classmethod
    def check_metrics_increase(cls, timestamp_metrics_sequence: List) -> None:
        """Return True if the average value of recent metrics is greater than the threshold"""
        _, metrics_sequence = zip(*timestamp_metrics_sequence)
        cal_avg = lambda sequence: sum(sequence) / len(sequence)
        
        boundaly = int(Config.METRICS_SEQUENCE_LENGTH*0.2)
        new_metrics_average = cal_avg(metrics_sequence[:boundaly])
        old_metrics_average = cal_avg(metrics_sequence[boundaly:Config.METRICS_SEQUENCE_LENGTH])
        
        metrics_increase = new_metrics_average * Config.THRESHOLD_RATE > old_metrics_average
        if metrics_increase:
            return True

        logger.info('There are no problems with recent metrics')    
        return False
    
    @classmethod
    def _get_latest_time(cls, timestamp_sequence: List) -> datetime.datetime:
        """Get latest time because latest time could be a minute ago due to processing time"""
        current_time = datetime.datetime.now().replace(second=0).replace(microsecond=0)
        if timestamp_sequence[0] == current_time:
            latest_time = current_time
        else:
            latest_time = current_time - datetime.timedelta(minutes=1)
        return latest_time
    
    @classmethod
    def _record_num_is_enough(cls, timestamp_sequence: List) -> bool:
        """Return True if three missing values follow"""
        if len(timestamp_sequence) < Config.METRICS_SEQUENCE_LENGTH - Config.ALLOWABLE_NUMBER_OF_FAILURES:
            return False
        
        latest_time = cls._get_latest_time(timestamp_sequence)
        target_datetime_list = [latest_time - datetime.timedelta(minutes=i) for i in range(Config.METRICS_SEQUENCE_LENGTH)]

        count = 0
        index = 0
        for target_datetime in target_datetime_list:
            if target_datetime == timestamp_sequence[index]:
                count = 0
                index += 1
            else:
                count += 1
            if count == Config.ALLOWABLE_NUMBER_OF_FAILURES:
                return False
            
        return True
    
    @classmethod
    def _timestamp_metrics_unzip(cls, timestamp_metrics_sequence: List) -> Tuple[List, List]:
        timestamp_sequence, metrics_sequence = zip(*timestamp_metrics_sequence)
        return list(timestamp_sequence), list(metrics_sequence)