#!/bin/bash

cd rest-api
docker build -t flask-app .
cd ../worker
docker build -t worker-app .
cd ..

docker run -d -p 5672:5672 -p 8080:15672 --hostname bus-rabbit --name bus-rabbit rabbitmq:3-management
docker run --name db-redis -d redis
docker run --name dk-keystone -p 35357:35357 -p 5000:5000 -d garland/docker-openstack-keystone

echo "Waiting Keystone to launch on 35357..."

while ! nc -z localhost 35357; do   
  sleep 1 # wait for 1/10 of the second before check again
done

while ! curl -H "X-Auth-Token:7a04a385b907caca141f" http://localhost:35357/v2.0/users; do   
  sleep 1 # wait for 1/10 of the second before check again
done

# create my user
curl -X POST \
    -H "X-Auth-Token:7a04a385b907caca141f" \
    -H "Content-type: application/json" \
    -d '{"user":{"name":"Joe","email":"joe@example.com.com","enabled":true,"password":"1234"}}' \
    http://localhost:35357/v2.0/users

# create my project
curl -X POST \
    -H "X-Auth-Token:7a04a385b907caca141f" \
    -H "Content-type: application/json" \
    -d '{"project": {"description": "RET automation edge project","enabled": true,"is_domain": true,"name": "ret-automation-edge"}}' \
    http://localhost:35357/v3/projects

# list all user
curl -H "X-Auth-Token:7a04a385b907caca141f" http://localhost:35357/v2.0/users

docker run --name restapi-inst \
    -p 5001:5000 \
    --link bus-rabbit \
    --link dk-keystone \
    -d flask-app

 docker run --name worker-inst \
    --link bus-rabbit \
    --link db-redis \
    -it worker-app