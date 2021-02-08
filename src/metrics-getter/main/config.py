from logging import DEBUG, INFO, WARNING, ERROR
import os


class Config(object):
    
    PAGE_SPEED_INSIGHTS_API_URI = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
    TARGET_WEB_PAGE_URI = os.environ.get('TARGET_WEB_PAGE_URI')
    PLATFORM = os.environ.get('PLATFORM')
    
    ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST')
    ELASTICSEARCH_PORT = os.environ.get('ELASTICSEARCH_PORT')
    ELASTICSEARCH_URL = f'http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}'
    
    INDEX_PREFIX = 'pagespeed-metrics-'
    INDEX_TEMPLATE_NAME = f'pagespeed-metrics-index-template'
    INDEX_TEMPLATE_PATH = './index_template.json'
    
    LOG_LEVEL_DICT = {'DEBUG': DEBUG, 'INFO': INFO, 'WARNING': WARNING, 'ERROR': ERROR}
    LOG_LEVEL = LOG_LEVEL_DICT[os.environ.get('LOG_LEVEL')]