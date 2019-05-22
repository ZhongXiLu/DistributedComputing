#!/usr/bin/env bash
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
for SERVICE in ${ROOT_DIR}/services/*
do
    #docker-compose -f ${ROOT_DIR}/docker-compose-dev.yml exec $(basename ${SERVICE}) python manage.py test
    kubectl exec -it $(kubectl get pods --all-namespaces | grep $(basename ${SERVICE})'-' | awk '{print $2}') python manage.py test
done
