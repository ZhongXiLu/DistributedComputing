#!/usr/bin/env bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Recreate and seed the database for each service
for SERVICE in ${ROOT_DIR}/services/*
do
    echo "Recreating database: $(basename ${SERVICE})"
    #docker-compose -f ${ROOT_DIR}/docker-compose-dev.yml exec $(basename ${SERVICE}) python manage.py recreate_db
    #docker-compose -f ${ROOT_DIR}/docker-compose-dev.yml exec $(basename ${SERVICE}) python manage.py seed_db
    kubectl exec -it $(kubectl get pods --all-namespaces | grep $(basename ${SERVICE})'-' | awk '{print $2}') python manage.py recreate_db
    kubectl exec -it $(kubectl get pods --all-namespaces | grep $(basename ${SERVICE})'-' | awk '{print $2}') python manage.py seed_db
done
