class ConnectionCloseError(Exception):
    """Error when failing to close the connection with Elasticsearch"""
    
class GetMetricsError(Exception):
    """Error to get metrics from Google PageSpeed Insights API"""
    
class IncorrectElasticsearchURLError(Exception):
    """Error when Elasticsearch URL is incorrect"""    

class IndexPatternConfirmError(Exception):
    """Error when failing to confirm index pattern of Elasticsearch"""

class IndexPatternCreationError(Exception):
    """Error when Elasticsearch fails to create index pattern"""

class MetricsInsertError(Exception):
    """Error when inserting data into Elasticsearch fails"""
    
