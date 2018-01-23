#!/bin/bash

kubectl delete -f minikube/redis.yaml
kubectl delete -f minikube/rabbitmq.yaml
kubectl delete -f minikube/keystone.yaml
kubectl delete -f minikube/restapi.yaml
kubectl delete -f minikube/reader.yaml
kubectl delete -f minikube/worker.yaml

ip_registry="eu.gcr.io/opteama-stelia"

gcloud container images delete --quiet $ip_registry/redis
gcloud container images delete --quiet $ip_registry/rabbitmq:3-management
gcloud container images delete --quiet $ip_registry/docker-openstack-keystone
gcloud container images delete --quiet $ip_registry/flask-app
gcloud container images delete --quiet $ip_registry/reader-app
gcloud container images delete --quiet $ip_registry/worker-app

gcloud container clusters delete kubernetes-lab1 --zone europe-west1-d
