#!/bin/bash

export TARGET_WEB_PAGE_URI=https://www.google.com/
export PLATFORM=desktop

export ELASTICSEARCH_HOST=localhost
export ELASTICSEARCH_PORT=30000

export LOG_LEVEL=INFO

python3 main.py
