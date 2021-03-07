
class ConnectionCloseError(Exception):
    """Error when failing to close the connection with Elasticsearch"""
    
class EnoughMetricsNotExists(Exception):
    """Error generated when not enough metrics exists"""

class IncorrectElasticsearchURLError(Exception):
    """Error when Elasticsearch URL is incorrect"""  
    
class MetricsDownError(Exception):
    """Error that occurs when the metrics down"""  

class SendAlertByWebhookError(Exception):
    """Error when failing to send alert by webhook"""
    
class GetTimestampMetricsSequenceError(Exception):
    """Error when failing to get timestamp and metrics sequence from Elasticsearch"""