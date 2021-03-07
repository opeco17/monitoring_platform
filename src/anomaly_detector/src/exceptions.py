
class ConnectionCloseError(Exception):
    """Error when failing to close the connection with Elasticsearch"""

class IncorrectElasticsearchURLError(Exception):
    """Error when Elasticsearch URL is incorrect"""  

class SendAlertByWebhookError(Exception):
    """Error when failing to send alert by webhook"""
    
class GetTimestampMetricsSequenceError(Exception):
    """Error when failing to get timestamp and metrics sequence from Elasticsearch"""