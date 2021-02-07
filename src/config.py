import os


class Config(object):
    
    PAGE_SPEED_INSIGHTS_API_URI = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
    TARGET_WEB_PAGE_URI = os.environ.get('TARGET_WEB_PAGE_URI')
    PLATFORM = os.environ.get('PLATFORM')
    
    ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST')
    ELASTICSEARCH_PORT = os.environ.get('ELASTICSEARCH_PORT')