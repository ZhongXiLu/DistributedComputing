
### Distributed Computing

Group 6:
- Zhong-Xi Lu
- Angela Mizero
- Thomas Van Bogaert


### Documentation

The documentation can be found in the [report](report/report.pdf).

### Setup

Get `kompose`:
```bash
curl -L https://github.com/kubernetes/kompose/releases/download/v1.18.0/kompose-linux-amd64 -o kompose
chmod +x kompose
```

Build and push images to DockerHub:
1. Export docker-hub username (used in docker-compose file): `export DOCKER_USERNAME=<username>`
2. Store docker-hub user credentials: `docker login`
3. Build and push all images using `kompose`: `kompose -f docker-compose-dev-kube.yml up`

Set up the services in kubernetes:
1. Start minikube in the background: `minikube start --memory=8192 --cpus=4`
2. Create pods: `kubectl create -f export/`
