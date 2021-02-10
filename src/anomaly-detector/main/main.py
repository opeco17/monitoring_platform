import datetime
import json
import sys
import time
from typing import Dict, List, Tuple

from elasticsearch import Elasticsearch
import requests
from requests.exceptions import HTTPError
from retry import retry

from config import Config
from logger import get_logger


logger = get_logger()


@retry(exceptions=HTTPError, tries=5, delay=3, logger=logger)
def send_alert(text: str, username: str) -> None:
    data = json.dumps({
        'text': text, 
        'username': username
    })
    
    response = requests.post(Config.WEBHOOK_URL, data=data)
    logger.info(f'Webhook Status Code: {response.status_code}')
    response.raise_for_status()
    return response


def create_search_query() -> Dict:
    """Create search query to get metrics from Elasticsearch"""
    with open(Config.SEARCH_QUERY_FILE) as search_query_file:
        search_query = json.load(search_query_file)

    search_query['query']['bool']['filter'][0]['term']['target_url'] = Config.TARGET_WEB_PAGE_URI
    search_query['query']['bool']['filter'][1]['term']['platform'] = Config.PLATFORM
    search_query['aggs']['histogram']['aggs']['metrics_average']['avg']['field'] = Config.ALERT_TARGET_METRICS
    search_query['aggs']['histogram']['aggs']['timestamp_sort']['bucket_sort']['size'] = Config.METRICS_SEQUENCE_LENGTH
    
    logger.debug('----------------------------Search Query----------------------------')
    logger.debug(search_query)
    logger.debug('--------------------------------------------------------------------')
    
    return search_query


def get_latest_time_in_sequence(timestamp_sequence:List) -> datetime.datetime:
    """Get latest time because latest time could be a minute ago due to processing time"""
    current_time = datetime.datetime.now().replace(second=0).replace(microsecond=0)
    if timestamp_sequence[0] == current_time:
        latest_time = current_time
    else:
        latest_time = current_time - datetime.timedelta(minutes=1)
    return latest_time
            

def search_metrics_sequence(elasticsearch: Elasticsearch) -> Tuple:
    """Get page speed metrics from Elasticsearch"""
    index_name = f'{Config.INDEX_PREFIX}-*'
    search_query = create_search_query()
    result = elasticsearch.search(index=index_name, body=search_query)
    if not result['_shards']['failed'] == 0:
        logger.info('Failed to get metrics from Elasticsearch.')
        sys.exit(1)
        
    logger.info('Get metrics from Elasticsearch successfully.')
    
    # Order of these sequence is desc ([latest, ..., oldest]).
    metrics_sequence = [record['metrics_average']['value'] for record in result['aggregations']['histogram']['buckets']]
    timestamp_sequence = [datetime.datetime.fromtimestamp(record['key'] // 1000) for record in result['aggregations']['histogram']['buckets']]
    return metrics_sequence, timestamp_sequence

def check_obtained_records(timestamp_sequence:List) -> None:
    """Check whether the sequence is obtained correctly"""
    latest_time = get_latest_time_in_sequence(timestamp_sequence)
        
    failure_count = 0
    failure = False
    target_time = latest_time
    for i in range(len(timestamp_sequence)):
        if timestamp_sequence[i] != target_time:
            failure_count += 1

        if failure_count > Config.ALLOWABLE_NUMBER_OF_FAILURES:
            failure = True
            break
        
        target_time -= datetime.timedelta(minutes=1)
        
    if not failure:
        logger.info('Obtained sequence records OK')
        return

    alert_text = f'Missing values followed {Config.ALLOWABLE_NUMBER_OF_FAILURES} times continuously.\n'
    alert_text += f'Please confirm metrics in {str(timestamp_sequence[i-Config.ALLOWABLE_NUMBER_OF_FAILURES])} ~ {str(timestamp_sequence[i])}.'
    alert_username = '[Error] Metrics not exist'
    logger.error(alert_text)
    try:
        send_alert(alert_text, alert_username)
        logger.info('Send webhook alert succeeded.')
        sys.exit(0)
    except HTTPError:
        logger.error('Send webhook alert failed.')
        sys.exit(1)
        
        
def fill_missing_value(metrics_sequence: List, timestamp_sequence: List) -> Tuple:
    """Fill missing value in sequence with interpolation"""
    latest_time = get_latest_time_in_sequence(timestamp_sequence)
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
    filled_timestamp_sequence, filled_metrics_sequence = zip(* sorted(zip(filled_timestamp_sequence, filled_metrics_sequence), reverse=True))
    return list(filled_metrics_sequence), list(filled_timestamp_sequence)

    
def anomaly_detection(metrics_sequence: List, timestamp_sequence: List) -> None:
    cal_avg = lambda sequence: sum(sequence) / len(sequence)
    
    boundaly = int(Config.METRICS_SEQUENCE_LENGTH*0.2)
    new_metrics_average = cal_avg(metrics_sequence[:boundaly])
    old_metrics_average = cal_avg(metrics_sequence[boundaly:Config.METRICS_SEQUENCE_LENGTH])
    
    anomalous = new_metrics_average * Config.THRESHOLD_RATE > old_metrics_average
    if not anomalous:
        logger.info('There are no ploblems.')
        return

    alert_text = f'Metrics sharply increased.\n'
    alert_text += f'Please confirm metrics in {str(timestamp_sequence[boundaly])} ~ {str(timestamp_sequence[0])}.'
    alert_username = '[Error] Metrics sharply increased'
    logger.error(alert_text)
    try:
        send_alert(alert_text, alert_username)
        logger.info('Send webhook alert succeeded.')
        sys.exit(0)
    except HTTPError:
        logger.error('Send webhook alert failed.')
        sys.exit(1)


def main() -> None:
    elasticsearch = Elasticsearch(Config.ELASTICSEARCH_URL)
    metrics_sequence, timestamp_sequence = search_metrics_sequence(elasticsearch)
    check_obtained_records(timestamp_sequence)
    metrics_sequence, timestamp_sequence = fill_missing_value(metrics_sequence, timestamp_sequence)
    anomaly_detection(metrics_sequence, timestamp_sequence)
    elasticsearch.close()
    

if __name__ == '__main__':
    logger.debug('----------------------------Config----------------------------')
    for key, value in Config.__dict__.items():
        logger.debug(f'{key}: {value}')
    logger.debug('--------------------------------------------------------------')
    
    main()