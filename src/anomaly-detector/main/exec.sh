#!/bin/bash

export TARGET_WEB_PAGE_URI=https://www.google.com/
export PLATFORM=mobile

export ELASTICSEARCH_URL=http://localhost:30000

export LOG_LEVEL=INFO

export INDEX_PREFIX=pagespeed-metrics
export INDEX_TEMPLATE_NAME=pagespeed-metrics-index-template
export SEARCH_QUERY_FILE=search_query.json
export ALERT_TARGET_METRICS=server_response_time
export METRICS_SEQUENCE_LENGTH=15
export ALLOWABLE_NUMBER_OF_FAILURES=3
export WEBHOOK_URL=https://hooks.slack.com/services/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

python3 main.py
