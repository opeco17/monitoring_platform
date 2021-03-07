from retry import retry

import json
import requests
from requests.models import Response
from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import Config
from exceptions import *
from logger import logger


class AlertSender:

    def send_alert(cls, text: str, username: str) -> None:
        data = json.dumps({
            'text': text, 
            'username': username
        })
        try:
            response = cls._post_request_with_retry(data=data)
        except (ConnectionError, HTTPError, Timeout):
            raise SendAlertByWebhookError
        else:
            return response
    
    @classmethod
    @retry(exceptions=(ConnectionError, HTTPError, Timeout), tries=3, delay=3, logger=logger)
    def _post_request_with_retry(cls, data: str) -> Response:
        response = requests.post(Config.WEBHOOK_URL, data=data)
        logger.info(f'Webhook Status Code: {response.status_code}')
        response.raise_for_status()
        return response