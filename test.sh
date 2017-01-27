#!/bin/bash

while ! curl -X POST -v \
    --connect-timeout 1 --max-time 10 \
    -H "X-Auth-Token:7a04a385b907caca141f" \
    -H "Content-type: application/json" \
    -d '{"user":{"name":"Joe","email":"joe@example.com.com","enabled":true,"password":"1234"}}' \
    http://$(minikube ip):$(kubectl get service keystone-management --output jsonpath='{.spec.ports[?(@.port==35357)].nodePort}')/v2.0/users; do

    sleep 1
done

