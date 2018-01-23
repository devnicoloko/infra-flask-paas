#!/bin/bash

docker pull redis
docker pull rabbitmq:3-management
docker pull garland/docker-openstack-keystone

cd rest-api && docker build -t flask-app . && cd ../worker && docker build -t worker-app .  && cd ../reader && docker build -t reader-app . && cd ..


ip_registry="eu.gcr.io/opteama-stelia"
docker tag redis $ip_registry/redis
docker tag rabbitmq:3-management $ip_registry/rabbitmq:3-management
docker tag garland/docker-openstack-keystone $ip_registry/docker-openstack-keystone
docker tag flask-app $ip_registry/flask-app
docker tag reader-app $ip_registry/reader-app
docker tag worker-app $ip_registry/worker-app

gcloud docker -- push $ip_registry/redis
gcloud docker -- push $ip_registry/rabbitmq:3-management
gcloud docker -- push $ip_registry/docker-openstack-keystone
gcloud docker -- push $ip_registry/flask-app
gcloud docker -- push $ip_registry/reader-app
gcloud docker -- push $ip_registry/worker-app

#gcloud container clusters create kubernetes-lab1   --disk-size 100   --zone europe-west1-d   --enable-cloud-logging   --enable-cloud-monitoring   --machine-type n1-standard-2   --num-nodes 3
#gcloud container clusters get-credentials kubernetes-lab1 --zone europe-west1-d

kubectl create -f minikube/redis.yaml
kubectl create -f minikube/rabbitmq.yaml
kubectl create -f minikube/keystone.yaml


echo "create apps..."
kubectl create -f minikube/restapi.yaml
kubectl create -f minikube/reader.yaml
kubectl create -f minikube/worker.yaml

sleep 60


KEYSTONE_EXTERNAL_IP=`kubectl describe services keystone | grep 'LoadBalancer Ingress' | awk '{print $3}'`

echo "external ip address : ${KEYSTONE_EXTERNAL_IP}"

echo "create user Joe"
while ! curl -X POST \
    --connect-timeout 1 --max-time 10 \
    -H "X-Auth-Token:7a04a385b907caca141f" \
    -H "Content-type: application/json" \
    -d '{"user":{"name":"Joe","email":"joe@example.com.com","enabled":true,"password":"1234"}}' \
    http://${KEYSTONE_EXTERNAL_IP}:35357/v2.0/users; do

    sleep 1
done

RESTAPI_EXTERNAL_IP=`kubectl describe services restapi | grep 'LoadBalancer Ingress' | awk '{print $3}'`

open http://${RESTAPI_EXTERNAL_IP}:5000/apidocs/index.html

# kubectl scale --replicas=10 deployments/worker-deployment

# curl -X DELETE -H "X-Auth-Token:7a04a385b907caca141f" http://$(minikube ip):$(kubectl get service keystone-management --output jsonpath='{.spec.ports[?(@.port==35357)].nodePort}')/v2.0/users/1ce8553ef4ca4f2fbc73efbca8723a2a
