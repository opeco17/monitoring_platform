from contextlib import contextmanager
from typing import List

from config import Config


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