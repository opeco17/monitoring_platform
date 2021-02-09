from logging import DEBUG, INFO, WARNING, ERROR
import os


class Config(object):
    
    PAGE_SPEED_INSIGHTS_API_URI = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
    TARGET_WEB_PAGE_URI = os.environ.get('TARGET_WEB_PAGE_URI')
    PLATFORM = os.environ.get('PLATFORM')
    
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    
    INDEX_PREFIX = os.environ.get('INDEX_PREFIX')
    INDEX_TEMPLATE_NAME = os.environ.get('INDEX_TEMPLATE_NAME')
    SEARCH_QUERY_FILE = os.environ.get('SEARCH_QUERY_FILE')
    ALERT_TARGET_METRICS = os.environ.get('ALERT_TARGET_METRICS')
    METRICS_SEQUENCE_LENGTH = os.environ.get('METRICS_SEQUENCE_LENGTH')
    
    LOG_LEVEL_DICT = {'DEBUG': DEBUG, 'INFO': INFO, 'WARNING': WARNING, 'ERROR': ERROR}
    LOG_LEVEL = LOG_LEVEL_DICT[os.environ.get('LOG_LEVEL')]