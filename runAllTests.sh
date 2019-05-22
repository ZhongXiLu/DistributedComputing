#!/usr/bin/env bash
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
for SERVICE in ${ROOT_DIR}/services/*
do
    #docker-compose -f ${ROOT_DIR}/docker-compose-dev.yml exec $(basename ${SERVICE}) python manage.py test
    POD=$(kubectl get pods --all-namespaces | grep $(basename ${SERVICE})'-' | grep -v 'db-' | awk '{print $2}')
    kubectl exec -it $POD python manage.py test
done
