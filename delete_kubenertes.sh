#!/bin/bash

minikube delete

rm -Rf ~/.kube 
rm -Rf ~/.minikube 

docker-machine rm registry-vm --force