#!/bin/bash

# Build docker image
base_path=$(pwd)
echo $base_path
for dir in 'metrics-getter' 'anomaly-detector'; do
    cd src/$dir
    chmod +x build.sh
    ./build.sh
    cd $base_path
done

# # Run Kubernetes
# kubectl apply -f kubernetes-manifests/general-config.yaml
# kubectl apply -f kubernetes-manifests/elasticsearch.yaml
# kubectl apply -f kubernetes-manifests/kibana.yaml

# # Wait to run Elasticsearch
# sleep 60

# kubectl apply -f kubernetes-manifests/metrics-getter.yaml

# # Wait to get a sufficient number of metrics
# sleep 180

# kubectl apply -f kubernetes-manifests/anomaly-detector.yaml
