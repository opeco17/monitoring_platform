import sys

from anomaly_detection import AnomalyDetector
from connect_es import ElasticsearchConnector
from exceptions import *
from logger import logger
from utils import show_config_contents


def main() -> None:
    show_config_contents()
    
    try:
        elasticsearch_connector = ElasticsearchConnector()
    except IncorrectElasticsearchURLError:
        logger.error('Failed to connect to Elasticsearch')
        logger.error('Elasticsearch URL is incorrect')
        sys.exit(1)
    
    try:
        timestamp_metrics_sequence = elasticsearch_connector.get_timestamp_metrics_sequence()
        AnomalyDetector.check_missing_record(timestamp_metrics_sequence)
        timestamp_metrics_sequence = AnomalyDetector.fill_missing_value(timestamp_metrics_sequence)
        AnomalyDetector.check_metrics_down(timestamp_metrics_sequence)
    except GetTimestampMetricsSequenceError:
        print('ロギング')
    except EnoughMetricsNotExists:
        print('通知する')
    except MetricsDownError:
        print('通知する')
    finally:
        elasticsearch_connector.close()
    

if __name__ == '__main__':    
    main()