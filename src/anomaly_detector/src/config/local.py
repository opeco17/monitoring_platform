from logging import DEBUG, INFO, WARNING, ERROR


class Config(object):
    
    PAGE_SPEED_INSIGHTS_API_URI = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
    TARGET_WEB_PAGE_URI = 'https://www.google.com/, https://www.amazon.com/, https://www.facebook.com/, https://www.apple.com/'
    PLATFORM = 'desktop'
    
    ELASTICSEARCH_URL = 'http://localhost:30000'
    
    INDEX_PREFIX = 'pagespeed-metrics'
    INDEX_TEMPLATE_NAME = 'pagespeed-metrics-index-template'
    SEARCH_QUERY_FILE = 'json/search_query.json'
    ALERT_TARGET_METRICS = 'server_response_time'
    METRICS_SEQUENCE_LENGTH = int('30')
    ALLOWABLE_NUMBER_OF_FAILURES = int('3')
    THRESHOLD_RATE = float('0.3')
    WEBHOOK_URL = 'https://hooks.slack.com/services/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'
    
    LOG_LEVEL_DICT = {'DEBUG': DEBUG, 'INFO': INFO, 'WARNING': WARNING, 'ERROR': ERROR}
    LOG_LEVEL = LOG_LEVEL_DICT['DEBUG']