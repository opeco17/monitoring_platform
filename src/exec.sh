#!/bin/bash

export TARGET_WEB_PAGE_URI=https://www.google.com/
export PLATFORM=desktop

export ELASTICSEARCH_HOST=elasticsearch
export ELASTICSEARCH_PORT=9200

chmod +x main.py
python3 main.py
