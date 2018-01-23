# Requirements

Test on GKE

Please configure your GCLOUD env.

# Configuration

Change the project configuration to match your env. 

Example :
* configure your gcloud project id
* configure your Google Registry in deploy\_kubernetes.sh and delete\_kubernetes.sh

# Installation

To deploy localy please use:

`deploy_kubernetes.sh`

To delete localy:

`delete_kubernetes.sh`

# Schema

On your GKE:
- infra: redis
- infra: rabbitmq
- infra: keystone
- app: restapi
- app: reader
- app: worker
