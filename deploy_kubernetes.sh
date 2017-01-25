#!/bin/bash

eval $(docker-machine env -u)
docker-machine create \
      --engine-env 'DOCKER_OPTS="-H unix:///var/run/docker.sock"' \
      --driver virtualbox \
      registry-vm

eval $(docker-machine env registry-vm)
docker run -d -p 5000:5000 --name registry registry:2
eval $(docker-machine env -u)

ip_registry=$(docker-machine ip registry-vm)
docker tag redis $ip_registry:5000/redis
docker tag rabbitmq:3-management $ip_registry:5000/rabbitmq:3-management
docker tag garland/docker-openstack-keystone $ip_registry:5000/docker-openstack-keystone
docker tag flask-app $ip_registry:5000/flask-app
docker tag reader-app $ip_registry:5000/reader-app
docker tag worker-app $ip_registry:5000/worker-app

docker push $ip_registry:5000/redis
docker push $ip_registry:5000/rabbitmq:3-management
docker push $ip_registry:5000/docker-openstack-keystone
docker push $ip_registry:5000/flask-app
docker push $ip_registry:5000/reader-app
docker push $ip_registry:5000/worker-app

minikube start --insecure-registry=$ip_registry:5000

kubectl create -f minikube/redis.yaml
kubectl create -f minikube/rabbitmq.yaml
kubectl create -f minikube/keystone.yaml

echo "Minikube ip: $(minikube ip)"
echo "Keystone port: $(kubectl get service keystone-management --output jsonpath='{.spec.ports[?(@.port==35357)].nodePort}')"

echo "Waiting Keystone to launch on 35357..."
while ! nc -z $(minikube ip) $(kubectl get service keystone-management --output jsonpath='{.spec.ports[?(@.port==35357)].nodePort}'); do   
  sleep 1 # wait for 1/10 of the second before check again
done

echo "Waiting RabbitMQ to launch on 15672..."
while ! nc -z $(minikube ip) $(kubectl get service rabbitmq-management --output jsonpath='{.spec.ports[?(@.port==15672)].nodePort}'); do   
  sleep 1 # wait for 1/10 of the second before check again
done

echo "create user Joe"
curl -X POST \
    --connect-timeout 1 \
    -H "X-Auth-Token:7a04a385b907caca141f" \
    -H "Content-type: application/json" \
    -d '{"user":{"name":"Joe","email":"joe@example.com.com","enabled":true,"password":"1234"}}' \
    http://$(minikube ip):$(kubectl get service keystone-management --output jsonpath='{.spec.ports[?(@.port==35357)].nodePort}')/v2.0/users


echo "create apps..."
kubectl create -f minikube/restapi.yaml
kubectl create -f minikube/reader.yaml
kubectl create -f minikube/worker.yaml

echo "RabbitMQ: http://$(minikube ip):$(kubectl get service rabbitmq-management --output jsonpath='{.spec.ports[?(@.port==15672)].nodePort}')"
echo "REST API Swagger: http://$(minikube ip):$(kubectl get service restapi-service --output jsonpath='{.spec.ports[?(@.port==5000)].nodePort}')/apidocs/index.html"

minikube dashboard


# kubectl scale --replicas=3 deployments/worker-deployment

# curl -X DELETE -H "X-Auth-Token:7a04a385b907caca141f" http://$(minikube ip):$(kubectl get service keystone-management --output jsonpath='{.spec.ports[?(@.port==35357)].nodePort}')/v2.0/users/1ce8553ef4ca4f2fbc73efbca8723a2a
