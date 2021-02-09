#!/bin/bash

export TARGET_WEB_PAGE_URI=https://www.google.com/
export PLATFORM=desktop

export ELASTICSEARCH_URL=http://localhost:30000

export LOG_LEVEL=INFO

export INDEX_PREFIX=pagespeed-metrics
export INDEX_TEMPLATE_NAME=pagespeed-metrics-index-template
export SEARCH_QUERY_FILE=search_query.json
export ALERT_TARGET_METRICS=server_response_time
export METRICS_SEQUENCE_LENGTH=100

python3 main.py
