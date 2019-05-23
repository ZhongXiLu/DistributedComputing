
### Distributed Computing

Group 6:
- Zhong-Xi Lu
- Angela Mizero
- Thomas Van Bogaert


### Documentation

The documentation can be found in the [report](report/report.pdf).

### Setup

Note that step 1 and 2 can be skipped, since the images are prebuilt and publicly available on DockerHub.

1. Get `kompose` (in project root directory):
```bash
curl -L https://github.com/kubernetes/kompose/releases/download/v1.18.0/kompose-linux-amd64 -o kompose
chmod +x kompose
```

2. Build and push images to DockerHub (in project root directory):
    1. Export docker-hub username (used in docker-compose file): `export DOCKER_USERNAME=<username>`
    2. Store docker-hub user credentials: `docker login`
    3. Build and push all images using `kompose`: `kompose -f docker-compose-dev-kube.yml up`

3. Set up the services in kubernetes (in project root directory):
    1. Start minikube in the background: `minikube start --memory=8192 --cpus=4`
    2. Create pods: `kubectl create -f export/`
    3. Set up: `./setup.sh`
    4. The url's to access the main and chat application can be found via following commands:
        ```bash
        minikube service frontend --url
        minikube service chat --url
        ```
