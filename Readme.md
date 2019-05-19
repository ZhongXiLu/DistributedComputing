
### Deploy images to Kubernetes

1. Start minikube in the background: `sudo minikube start --vm-driver=none`
2. Export docker-hub username: `export DOCKER_USERNAME=<username>`
3. Store docker-hub user credentials: `docker login`
4. Build and push all images (only do this once): `sudo kompose -f docker-compose-dev-kube.yml up`
5. Create dir for converted files: `mkdir export`
6. Convert docker-compose file: `kompose -f docker-compose-dev-kube.yml convert -o export`
7. Create pods: `sudo kubectl create -f export/`
8. Get details on specific pod: `sudo kubectl describe pod <pod_name>`

### Other

- To build+launch docker container:
    run `(sudo) buildDockerCompose.sh`

- To make life easier:
    run `source project.aliases`
    this will map `docker-compose -f docker-compose-dev.yml exec" to "dockerExec`
