# Requirements

Test on MACOSX, may be compatible on Linux ;-)

Please install:
- Kubectl: https://kubernetes.io/docs/getting-started-guides/kubectl/
- Minikube: https://kubernetes.io/docs/getting-started-guides/minikube/

# Installation

To deploy localy please use:

```deploy_kubernetes.sh```

To delete localy:

```delete_kubernetes.sh```

# Schema

On your host, two vms:
- "registry_vm" to pop a local Docker registry
- "minikube" to pop a local Kubernetes

On your Kubernetes:
- infra: redis
- infra: rabbitmq
- infra: keystone
- app: restapi
- app: reader
- app: worker