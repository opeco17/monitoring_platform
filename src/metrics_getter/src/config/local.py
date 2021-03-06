from logging import DEBUG, INFO, WARNING, ERROR


class Config:
    
    PAGE_SPEED_INSIGHTS_API_URI = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
    TARGET_WEB_PAGE_URI = 'https://www.google.com/, https://www.amazon.com/, https://www.facebook.com/, https://www.apple.com/'
    PLATFORM = 'desktop'
    
    ELASTICSEARCH_URL = 'http://localhost:30000'
    
    INDEX_PREFIX = 'pagespeed-metrics'
    INDEX_TEMPLATE_NAME = 'pagespeed-metrics-index-template'
    INDEX_TEMPLATE_FILE = 'json/index_template.json'
    
    LOG_LEVEL_DICT = {'DEBUG': DEBUG, 'INFO': INFO, 'WARNING': WARNING, 'ERROR': ERROR}
    LOG_LEVEL = LOG_LEVEL_DICT['DEBUG']
