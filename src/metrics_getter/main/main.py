import sys
from typing import Dict

from config import Config
from connect_es import ElasticsearchConnector
from exceptions import *
from get_metrics import MetricsGetter
from logger import logger


def show_config_contents() -> None:
    logger.debug('----------------------------Config----------------------------')
    for key, value in Config.__dict__.items():
        logger.debug(f'{key}: {value}')
    logger.debug('--------------------------------------------------------------')
    

def main() -> None:
    show_config_contents()
    
    try:
        metrics = MetricsGetter.get_page_speed_metrics()
        elasticsearch_connector = ElasticsearchConnector()
    except GetMetricsError:
        logger.error('Failed to get metrics from Google PageSpeed Insights API')
        sys.exit(1)
    except IncorrectElasticsearchURLError:
        logger.error('Failed to connect to Elasticsearch')
        logger.error('Elasticsearch URL is incorrect')
        sys.exit(1)
    
    try:
        elasticsearch_connector.create_index_template()
        elasticsearch_connector.insert(metrics)
    except IndexPatternConfirmError:
        logger.error('Failed to confirm index pattern of Elasticsearch')
        sys.exit(1)
    except IndexPatternCreationError:
        logger.error('Failed to create index pattern to Elasticsearch')
        sys.exit(1)
    except MetricsInsertError:
        logger.error('Failed to insert metrics to Elasticsearch')
        sys.exit(1)
    finally:
        elasticsearch_connector.close()
    

if __name__ == '__main__':        
    main()