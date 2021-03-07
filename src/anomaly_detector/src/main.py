import sys

from anomaly_detection import AnomalyDetector
from connect_es import ElasticsearchConnector
from exceptions import *
from logger import logger
from send_alert import AlertSender
from utils import get_web_page_url_list, show_config_contents


def main() -> None:
    show_config_contents()
    
    web_page_url_list = get_web_page_url_list()
    
    try:
        elasticsearch_connector = ElasticsearchConnector()
    except IncorrectElasticsearchURLError:
        logger.error('Failed to connect to Elasticsearch')
        logger.error('Elasticsearch URL is incorrect')
        sys.exit(1)
        
    try:
        for web_page_url in web_page_url_list:
            timestamp_metrics_sequence = elasticsearch_connector.get_timestamp_metrics_sequence(web_page_url)
            record_num_is_enough = AnomalyDetector.check_record_num_is_enough(timestamp_metrics_sequence)
            if not record_num_is_enough:
                AlertSender.send_alert_for_record_not_enough(web_page_url, timestamp_metrics_sequence)
                continue
                
            timestamp_metrics_sequence = AnomalyDetector.fill_missing_value(timestamp_metrics_sequence)
            
            metrics_increase = AnomalyDetector.check_metrics_increase(timestamp_metrics_sequence)
            if metrics_increase:
                AlertSender.send_alert_for_metrics_increase(web_page_url, timestamp_metrics_sequence)
                continue
                         
    except GetTimestampMetricsSequenceError:
        logger.error('Failed to get timestamp metrics sequence from Elasticsearch')
        sys.exit(1)
    except SendAlertByWebhookError:
        logger.error('Failed to send alert by webhook')
        sys.exit(1)
    finally:
        elasticsearch_connector.close()
    

if __name__ == '__main__':    
    main()