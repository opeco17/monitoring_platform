from retry import retry
from typing import List

import json
import requests
from requests.models import Response
from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import Config
from exceptions import *
from logger import logger


class AlertSender:
    
    @classmethod
    def send_alert_for_record_not_enough(cls, web_page_url: str, timestamp_metrics_sequence: List) -> None:
        timestamp_sequence, _ = zip(*timestamp_metrics_sequence)
        alert_text = f'{web_page_url}\n'
        alert_text += f'Missing values followed {Config.ALLOWABLE_NUMBER_OF_FAILURES} times continuously.\n'
        alert_text += f'Please confirm metrics in {str(timestamp_sequence[0])} ~ {str(timestamp_sequence[-1])}.'
        alert_username = '[Error] Enough metrics not exists'
        cls._send_alert(alert_text, alert_username)
        
    @classmethod
    def send_alert_for_metrics_increase(cls, web_page_url: str, timestamp_metrics_sequence: List) -> None:
        timestamp_sequence, _ = zip(*timestamp_metrics_sequence)
        alert_text = f'{web_page_url}\n'
        alert_text += f'Missing values followed {Config.ALLOWABLE_NUMBER_OF_FAILURES} times continuously.\n'
        alert_text += f'Please confirm metrics in {str(timestamp_sequence[0])} ~ {str(timestamp_sequence[-1])}.'
        alert_username = '[Error] Enough metrics not exists'
        cls._send_alert(alert_text, alert_username)
        
    @classmethod
    def _send_alert(cls, text: str, username: str) -> None:
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