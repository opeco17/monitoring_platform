from contextlib import contextmanager
from typing import Any, List

from config import Config
from requests.exceptions import HTTPError


class ResponseMock:
    
    def __init__(self, status_code: int, body: Any):
        self.status_code = status_code
        self.body = body
        
    def json(self):
        return self.body
        
    def raise_for_status(self):
        if 200 <= self.status_code <= 299:
            return
        raise HTTPError
    
    
@contextmanager
def config_setup(config_attrs: List):
    try:
        old_config_attrs = [(key, getattr(Config, key)) for key, _ in config_attrs]
        for key, value in config_attrs:
            setattr(Config, key, value)
        yield None
    finally:
        for key, value in old_config_attrs:
            setattr(Config, key, value)